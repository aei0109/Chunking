"""
[ BI_error_corrector ]
2019-07-03
system적으로 걸러낼 수 있는 것은 완료(2019-07-28: _2로 분기, 본 모듈은 더 이상 사용X)
여기까지가 Chunk Tagger의 BI-error corrector module
Y. Namgoong
"""

from utils_saveNload import load_pickle_chr_pred

chk_pred = load_pickle_chr_pred() # chunk tagger로 예측한 결과물이자 toChunk-based_DepCorpus의 입력

for j, chk_sent in enumerate(chk_pred, 1):
    for i, chk in enumerate(chk_sent):
        # present morpheme info.
        bi_tag, chk_tag = chk.split('-')
        # next morpheme info.
        try:
            next_bi_tag, next_chk_tag = chk_sent[i+1].split('-')

            if bi_tag == "B" and next_bi_tag == "B":
                if len(chk_tag) == 2:
                    if next_chk_tag == chk_tag:  # B-NX, B-NX
                        pass
                    elif len(next_chk_tag) == 2:  # B-NX, B-PX
                        pass
                    elif len(next_chk_tag) == 3:  # B-NX, B-JKX
                        pass
                    else: pass
                elif len(chk_tag) == 3:
                    if next_chk_tag == chk_tag:  # B-JKX, B-JKX  # error1
                        if chk == 'B-SYX':
                            chk_sent[i+1] = 'I-SYX'
                    elif len(next_chk_tag) == 2:  # B-JKX, B-NX
                        pass
                    elif len(next_chk_tag) == 3:  # B-JKX, B-JUX
                        pass
                    else: pass
            elif bi_tag == "B" and next_bi_tag == "I":
                if len(chk_tag) == 2:
                    if next_chk_tag == chk_tag:  # B-NX, I-NX
                        pass
                    elif len(next_chk_tag) == 2:  # B-NX, I-PX  # error2
                        print("sent_id:", j)
                        print(chk_sent)
                        print(chk_sent[i+1], chk)
                        if chk_sent[i+1] == 'I-PX':
                            print(chk_sent)
                            chk_sent[i] = 'B-PX'
                            print(chk_sent)  # 여기서 save 해야함.
                            input()
                    elif len(next_chk_tag) == 3:  # B-NX, I-JKX  # error3
                        pass  # 수동 교정 할 계획
                    else: pass
                elif len(chk_tag) == 3:
                    if next_chk_tag == chk_tag:  # B-JKX, I-JKX
                        pass
                    elif len(next_chk_tag) == 2:  # B-JKX, I-NX  # error4
                        pass
                    elif len(next_chk_tag) == 3:  # B-JKX, I-JUX  # error5
                        if chk_sent[i] == 'B-SYX' and chk_sent[i+1] == 'I-ECX':
                            chk_sent[i] = 'I-ECX'
                            if chk_sent[i-1] == 'B-EFX':  # rage error 나는지 확인
                                chk_sent[i-1] = 'B-ECX'

                    else: pass
            elif bi_tag == "I" and next_bi_tag == "B":
                if len(chk_tag) == 2:
                    if next_chk_tag == chk_tag:  # I-NX, B-NX
                        pass
                    elif len(next_chk_tag) == 2:  # I-NX, B-PX
                        pass
                    elif len(next_chk_tag) == 3:  # I-NX, B-JKX
                        pass
                    else: pass
                elif len(chk_tag) == 3:
                    if next_chk_tag == chk_tag:  # I-JKX, B-JKX  # error6
                        chk_sent[i+1].split('-')[0] = 'I'
                    elif len(next_chk_tag) == 2:  # I-JKX, B-NX
                        pass
                    elif len(next_chk_tag) == 3:  # I-JKX, B-JUX
                        pass
                    else: pass
            elif bi_tag == "I" and next_bi_tag == "I":
                if len(chk_tag) == 2:
                    if next_chk_tag == chk_tag:  # I-NX, I-NX
                        pass
                    elif len(next_chk_tag) == 2:  # I-NX, I-PX  # error7
                        pass
                    elif len(next_chk_tag) == 3:  # I-NX, I-JKX  # error8
                        if chk == 'I-AX' and chk_sent[i+1] == 'I-JKX':
                            chk_sent[i+1] = 'I-AX'
                    else: pass
                elif len(chk_tag) == 3:
                    if next_chk_tag == chk_tag:  # I-JKX, I-JKX
                        pass
                    elif len(next_chk_tag) == 2:  # I-JKX, I-NX  # error9
                        pass
                    elif len(next_chk_tag) == 3:  # I-JKX, I-JUX  # error10
                        chk_sent[i+1] = 'I-' + chk_tag
                    else: pass
            else: pass
        except IndexError:  # be raised error when the final morpheme comes.
            # processing for the last morpheme
            if len(chk_tag) == 2:  # content words
                pass
            elif len(chk_tag) == 3:  # functional words
                pass
            else:  # for handling exceptions
                pass

    print("result: ", j, chk_sent)  # 여기서 save해도 됨.