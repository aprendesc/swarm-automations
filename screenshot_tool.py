def screenshot_tool(config):
    ################################################################################################################
    import io, base64
    from PIL import ImageGrab
    ################################################################################################################
    img = ImageGrab.grab()
    buf = io.BytesIO(); img.save(buf, format='PNG')
    config['result'] = {'screenshot_b64': base64.b64encode(buf.getvalue()).decode()}
    return config
