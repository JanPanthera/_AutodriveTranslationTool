def output(message, message_type="", loc_func=None, output_widget=None, console=False, loc_param_func=None, loc_params=None, logger=None):
    prefix = loc_func(message_type + "_prefix") if message_type and loc_func else ""
    prefix = "" if prefix == message_type + "_prefix" else prefix

    if loc_func and loc_params == "loc":
        message = loc_func(message)
    elif loc_func and not isinstance(loc_params, (list, tuple)):
        message = loc_param_func(message, loc_params)
    elif loc_param_func and isinstance(loc_params, (list, tuple)):
        message = loc_param_func(message, *loc_params)

    if logger:
        message = message.replace("\n", "")
        log_func = getattr(logger, message_type, logger.info)
        log_func(message)

    final_message = f"{prefix}: {message}\n" if prefix else f"{message}\n"

    if output_widget:
        output_widget.write_console(final_message)

    if console:
        print(final_message, end='')
