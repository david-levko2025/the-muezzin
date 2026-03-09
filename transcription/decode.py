import base64

class Decoder:
    def decoderBase64(self,encoded):
        decode = base64.b64decode(encoded)
        return decode.decode('ascii')
    
decoder = Decoder()

list_most_danger_to_israel = """
R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvb
ixSZWZ1ZVlcyxJQ0MsQkRT
"""

list_less_danger_to_israel = """
RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQY
Wxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ==
"""

the_most_danger_words = decoder.decoderBase64(list_most_danger_to_israel)
the_less_danger_words = decoder.decoderBase64(list_less_danger_to_israel)