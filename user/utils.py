import jwt


class EncodeDecodeToken:

    @staticmethod
    def encode_token(payload):
        encoded_token = jwt.encode(payload,
                                   "secret",
                                   algorithm="HS256"
                                   )
        return encoded_token

    @staticmethod
    def decode_token(token):
        decoded_token = jwt.decode(
            token,
            "secret",
            algorithms="HS256"
        )
        return decoded_token
