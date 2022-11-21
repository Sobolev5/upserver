from django.db.models import signals


def change_commands_syntax(sender, **kwargs):
    from monitoring.models import Monitor
        
    instance = kwargs["instance"]
    instance.su_restore_commands = ";".join([x.strip() for x in instance.su_restore_commands.split("\n")])

    signals.post_save.disconnect(change_commands_syntax, sender=Monitor)
    instance.save()
    signals.post_save.connect(change_commands_syntax, sender=Monitor)