import base64

class BDSAnalyzer:
    def __init__(self):
        most_danger_enc = "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"
        less_danger_enc = "RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="
        
        self.hostile_words = base64.b64decode(most_danger_enc).decode('ascii').lower().split(',')
        self.less_hostile_words = base64.b64decode(less_danger_enc).decode('ascii').lower().split(',')

    def analyze(self, text, threshold=5.0):
        if not text:
            return 0.0, False, "none"
        
        text = text.lower()
        score = 0
        total_words = len(text.split())

        for word in self.hostile_words:
            score += text.count(word.strip()) * 2
            
        for word in self.less_hostile_words:
            score += text.count(word.strip()) * 1

        percent_bds = min((score / max(total_words, 1)) * 100, 100.0)
        
        if percent_bds == 0: level = "none"
        elif percent_bds < threshold: level = "medium"
        else: level = "high"

        return round(percent_bds, 2), percent_bds >= threshold, level