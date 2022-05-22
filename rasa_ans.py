class response:
    def user_ans(self, ra_val):
        intention = ra_val["intent"]["name"]
        confidence = ra_val["intent"]["confidence"]
        if intention != "nlu_fallback":
            if confidence > 0.44:
                if intention == "ket_hon":
                    self.ans = self.ket_hon_re()
                elif intention == "nvqs":
                    self.ans = self.nvqs_re()
                elif intention == "giam_ho":
                    self.ans = self.giam_ho_re()
                elif intention == "ho_ngheo":
                    self.ans = self.ho_ngheo_re()
                elif intention == "di_chuc":
                    self.ans = self.di_chuc_re()
                elif intention =="kethon_tamtru":
                    self.ans = self.kethon_tamtru()
                elif intention == "tu_y_kethon":
                    self.ans = self.tu_y_kethon()
                elif intention == "thgian_nghi_kh":
                    self.ans = self.thgian_nghi_kh()
                elif intention == "hoan_nvqs":
                    self.ans = self.hoan_nvqs()
                elif intention == "congchung_dichuc":
                    self.ans = self.congchung_dichuc()
                elif intention == "dk_giamho":
                    self.ans = self.dk_giamho()
            else:
                self.ans = self.fail()
        else:
            self.ans = self.fail()
        return self.ans

    # def task(self, ra_val):
    #     intention = ra_val["intent"]["name"]
    #     confidence = ra_val["intent"]["confidence"]
    #     if intention != "nlu_fallback":
    #         if confidence > 0.7:
    #             if intention == "ket_hon":
    #                 self.title = "Đăng ký kết hôn"
    #             elif intention == "nvqs":
    #                 self.title = "Đăng ký nghĩa vụ quân sự"
    #             elif intention == "giam_ho":
    #                 self.title = "Đăng ký giám hộ"
    #             elif intention == "ho_ngheo":
    #                 self.title = "Đăng ký xác nhận hộ nghèo"
    #             elif intention == "di_chuc":
    #                 self.title = "Chứng thực di chúc"
    #         else:
    #             pass
    #         return self.title

    ## responses
    def ket_hon_re(self):
        f = open('replies/ket_hon.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def nvqs_re(self):
        f = open('replies/nvqs.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def giam_ho_re(self):
        f = open('replies/giam_ho.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def ho_ngheo_re(self):
        f = open('replies/ho_ngheo.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def di_chuc_re(self):
        f = open('replies/di_chuc.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def fail(self):
        self.response = "dang cap nhat"
        return self.response

    def kethon_tamtru(self):
        f = open('replies/fq/kethon_tamtru.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def tu_y_kethon(self):
        f = open('replies/fq/tu_y_kethon.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def thgian_nghi_kh(self):
        f = open('replies/fq/thgian_nghi_kh.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def hoan_nvqs(self):
        f = open('replies/fq/hoan_nvqs.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def congchung_dichuc(self):
        f = open('replies/fq/congchung_dichuc.txt', encoding='utf-8')
        self.response = f.read()
        return self.response

    def dk_giamho(self):
        f = open('replies/fq/dk_giamho.txt', encoding='utf-8')
        self.response = f.read()
        return self.response