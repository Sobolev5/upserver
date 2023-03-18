#[macro_use]
extern crate reqwest;
use postgres::{Client, NoTls};
use std::env;
use std::{thread, time};
use std::net::TcpStream;
use ssh2::Session;
use std::io::prelude::*;
use chrono::prelude::*;
use std::error::Error;


pub struct Monitor {
    id: i64,
    name: String,
    host: String,
    port: i32,
    su_host: String,
    su_port: i32,
    su_login: String,
    su_password: String,
    su_restore_commands: String,
    restore_hops: i32
}


fn main() {
    let time_sleep = time::Duration::from_secs(30);
    loop {
        println!("main: start infinity loop [*]");            
        match get_database_records() {
            Ok(monitor_data) => { 
                for monitor in monitor_data {
                    println!("\n\nmain: monitor {} {} restore_hops={}", monitor.name, monitor.host, monitor.restore_hops);
                    match do_request(&monitor) {
                        Ok(response_status) => {
                            println!("main: response from {} {} {} repair restore_hops={}", monitor.name, monitor.host, response_status, monitor.restore_hops);
                            update_restore_hops(&monitor, 0).unwrap();
                            let available = true;
                            match write_monitor_activity_log(&monitor, &response_status, available) {
                                Ok(_) => { 
                                    println!("main: write_monitor_activity_log [HOST OK]");
                                },                                   
                                Err(e) => {
                                    println!("main: write_monitor_activity_log error error={}", e);
                                }
                            }                    
                        },
                        Err(e) => {
                            eprintln!("main: no response {} {} {} repair restore_hops={}", monitor.name, monitor.host, e, monitor.restore_hops); 
                            let error = format!("error {}", e); 
                            let available = false;
                            match write_monitor_activity_log(&monitor, &error, available) {
                                Ok(_) => { 
                                    println!("main: write_monitor_activity_log [HOST NOT OK]");
                                },                                   
                                Err(e) => {
                                    println!("main: write_monitor_activity_log error error={}", e);
                                }
                            }     

                            if monitor.restore_hops > 5 {
                                match do_repair(&monitor) {
                                    Ok(_) => { 
                                        println!("main: do_repair");
                                    },                                
                                    Err(e) => {
                                        println!("main: do_repair error={}", e);
                                    }
                                }
                                update_restore_hops(&monitor, 0).unwrap();
                            } else {
                                let restore_hops = monitor.restore_hops + 1;
                                update_restore_hops(&monitor, restore_hops).unwrap();  
                            }
                        }      
                    }
                }                         
            },
            Err(e) => { 
                eprintln!("main: db not ok {} ************************************************************************************", e); 
                continue;
            },
        }     
        thread::sleep(time_sleep);
    }
}


fn get_database_records() -> Result<Vec<Monitor>, postgres::Error> {
    let mut monitor_data:Vec<Monitor> = Vec::new();
    let connect_string = format!("postgres://{}:{}@{}:{}/{}", env!("POSTGRES_USER"), env!("POSTGRES_PASSWORD"), env!("POSTGRES_HOST"), env!("POSTGRES_PORT"), env!("POSTGRES_DB"));   
    println!("get_database_records: {}", connect_string);
    let mut client = Client::connect(&connect_string, NoTls)?;
    for row in client.query("SELECT * FROM public.monitoring_monitor", &[])? {
        let active: bool = row.get("active");
        if active == true {
            let monitor = Monitor { 
                id: row.get("id"),
                name: row.get("name"),
                host: row.get("host"),
                port: row.get("port"),
                su_host: row.get("su_host"),
                su_port: row.get("su_port"),
                su_login: row.get("su_login"),
                su_password: row.get("su_password"),
                su_restore_commands: row.get("su_restore_commands"), 
                restore_hops: row.get("restore_hops")               
            };
            monitor_data.push(monitor);   
        }     
    }    
    Ok(monitor_data)
}


fn do_request(monitor: &Monitor) -> Result<String, Box<dyn Error>> {
    let monitor_http: std::string::String;
    let socket: std::string::String;
    let response_status: std::string::String;

    if monitor.port == 443 {
        monitor_http = format!("https://{}:{}", monitor.host, monitor.port)
    } else {
        monitor_http = format!("http://{}:{}", monitor.host, monitor.port)  
    }
    socket = format!("{}:{}", monitor.host, monitor.port);

    println!("do_request: {} {} {}", monitor_http, monitor.name, monitor.host);
    match reqwest::blocking::get(&monitor_http) {
        Ok(response) => { 
            println!("do_request: reqwest::blocking::get [OK]");
            response_status = response.status().to_string();
            println!("do_request: {} reqwest::response_status {}", monitor.name, response_status);   
            if response_status == "502 Bad Gateway".to_string() {
                Err("502 Bad Gateway".to_string())?
            } else {
                Ok(response_status)
            }
        },
        Err(_e) => {
            println!("do_request: reqwest::blocking::get [NOT OK], try TCP connection");
            if let Ok(_stream) = TcpStream::connect(socket) {
                response_status = "TcpStream OK".to_string();
                Ok(response_status)
            } else {
                Err("TcpStream NOT OK".to_string())?
            }          
        }
    }       
}


fn update_restore_hops(monitor: &Monitor, restore_hops: i32) -> Result<(), Box<dyn Error>> {
    let connect_string = format!("postgres://{}:{}@{}:{}/{}", env!("POSTGRES_USER"), env!("POSTGRES_PASSWORD"), env!("POSTGRES_HOST"), env!("POSTGRES_PORT"), env!("POSTGRES_DB")); 
    println!("update_restore_hops: {} {}", monitor.name, connect_string);
    let mut client = Client::connect(&connect_string, NoTls)?;
    client.execute(
        "UPDATE public.monitoring_monitor SET restore_hops = $1 WHERE id = $2", &[&restore_hops, &monitor.id],
    )?;
    Ok(())
}


fn write_monitor_activity_log(monitor: &Monitor, response: &String, available: bool) -> Result<(), Box<dyn Error>> {
    let connect_string = format!("postgres://{}:{}@{}:{}/{}", env!("POSTGRES_USER"), env!("POSTGRES_PASSWORD"), env!("POSTGRES_HOST"), env!("POSTGRES_PORT"), env!("POSTGRES_DB")); 
    println!("write_monitor_activity_log: {} {}", monitor.name, connect_string);
    let mut client = Client::connect(&connect_string, NoTls)?;
    let utc: DateTime<Utc> = Utc::now();
    let utc_to_string = format!("{}", utc.to_string());
    client.execute(
        "INSERT INTO public.monitoring_monitoractivity (monitor_id, server_response, server_available, creation_date) VALUES ($1, $2, $3, $4)",
        &[&monitor.id, &response, &available, &utc_to_string],
    )?;
    Ok(())
}


fn do_repair(monitor: &Monitor) -> Result<(), Box<dyn Error>> {
    let connect_string = format!("postgres://{}:{}@{}:{}/{}", env!("POSTGRES_USER"), env!("POSTGRES_PASSWORD"), env!("POSTGRES_HOST"), env!("POSTGRES_PORT"), env!("POSTGRES_DB"));
    println!("do_repair: {} {} {}",monitor.name, monitor.host, connect_string);
    let su_host = format!("{}:{}", monitor.su_host, monitor.su_port);
    let su_restore_commands = format!("{}", monitor.su_restore_commands);
    println!("{}", su_restore_commands);
    let tcp = TcpStream::connect(su_host)?;
    let mut sess = Session::new()?;
    sess.set_tcp_stream(tcp);
    sess.handshake()?;
    let utc: DateTime<Utc> = Utc::now();
    let utc_to_string = format!("{}", utc.to_string());
    let mut client = Client::connect(&connect_string, NoTls)?;  
    match sess.userauth_password(&monitor.su_login, &monitor.su_password) {
        Ok(_) => { 
            println!("main: write_monitor_activity_log success");
            let mut channel = sess.channel_session()?;
        
            channel.exec(&su_restore_commands)?;
            let mut console_log = String::new();
            channel.read_to_string(&mut console_log)?;
            channel.wait_close()?;
            let exit_status: std::string::String;
            exit_status = format!("{}", channel.exit_status()?);            
            println!("channel status: {}", exit_status);

            client.execute(
                "INSERT INTO public.monitoring_restoreactivity (monitor_id, console_log, exit_status, creation_date) VALUES ($1, $2, $3, $4)",
                &[&monitor.id, &console_log, &exit_status, &utc_to_string],
            )?;
        },                                   
        Err(_e) => {
            let error_log: std::string::String;
            error_log = format!("Monitor {} error auth", monitor.name);
            client.execute(
                "INSERT INTO public.monitoring_restoreactivity (monitor_id, console_log, creation_date) VALUES ($1, $2, $3)",
                &[&monitor.id, &error_log, &utc_to_string],
            )?;
        }
    }
    Ok(())
}   

