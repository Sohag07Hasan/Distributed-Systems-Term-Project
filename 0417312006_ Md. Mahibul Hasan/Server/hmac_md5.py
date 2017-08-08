import hmac
def hmac_md5(key, message):
    encrypted_message = ''
    try:
        key = bytes(str(key), 'UTF-8')
        message = bytes(str(message), 'UTF-8')
        digest_maker = hmac.new(key, message)
        encrypted_message = digest_maker.hexdigest()
    except:
        pass
    return encrypted_message
