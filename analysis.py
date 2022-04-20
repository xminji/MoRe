from datetime import datetime
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from konlpy.tag import Okt
from collections import Counter
from PIL import Image
import numpy as np




def getWordCloudImg(mYear,mId):
    posTagger = Okt()
    # 1. 해당 영화의 리뷰를 모두 불러온다.
    file_read = open("data/review/{0}_review.csv".format(mYear), "r", encoding='UTF8')

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    reviewText_Positive = ""
    reviewText_Negative = ""
    for row in f_reader_Arr:
        if str(row[0]) == str(mId):
            if int(row[1]) > 5:
                reviewText_Positive = reviewText_Positive + " " + str(row[2])
            else:
                reviewText_Negative = reviewText_Negative + " " + str(row[2])



    # 2. Positive / 워드클라우드를 그린다.
    sentences_tag = []
    sentences_tag_po = posTagger.pos(reviewText_Positive)
    sentences_tag_ne = posTagger.pos(reviewText_Negative)

    for tag_po_ne in sentences_tag_po, sentences_tag_ne:
        if len(tag_po_ne) == 0:
            tag_po_ne.append(('정보 없음','Noun'))
        noun_adj_list = []
        for word, tag in tag_po_ne:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)

        # 특정 단어 제거
        delWord = ['영화','평점','다시','그','난','입니다','퍈','이영화','관람','관람객']
        noun_adj_list = [i for i in noun_adj_list if i not in delWord]

        counts = Counter(noun_adj_list)
        tags = counts.most_common(100)


        # 마스크가 될 이미지 불러오기
        if tag_po_ne == sentences_tag_po:
            icon = Image.open('static/img/wordLike.png')

            mask = Image.new( "RGB", icon.size, (255, 255, 255) )
            mask.paste(icon, icon)
            mask = np.array(mask)
            wc = WordCloud( font_path='C:\Windows\Fonts\MALGUNBD.TTF',  # 폰트
                            background_color='black',  # 배경색
                            colormap='winter',
                            mask=mask )  # 마스크설정

            cloud = wc.generate_from_frequencies( dict( tags ) )  # 사전형태의 데이터

            wordCloudImgPath_po = "static/images/wordCloudImg_po.jpg"

            cloud.to_file( wordCloudImgPath_po )
        else:
            icon = Image.open( 'static/img/wordDisLike.png' )

            mask = Image.new( "RGB", icon.size, (255, 255, 255) )
            mask.paste( icon, icon )
            mask = np.array( mask )
            wc = WordCloud( font_path='C:\Windows\Fonts\MALGUNBD.TTF',  # 폰트
                            background_color='black',  # 배경색
                            colormap='gist_heat',
                            mask=mask )  # 마스크설정

            cloud = wc.generate_from_frequencies( dict( tags ) )  # 사전형태의 데이터

            wordCloudImgPath_ne = "static/images/wordCloudImg_ne.jpg"

            cloud.to_file(wordCloudImgPath_ne)


    return wordCloudImgPath_po, wordCloudImgPath_ne




if __name__ == "__main__":
    print("[" + str(datetime.now()) + "] WordCloud Started..")

    getWordCloudImg(2011, 70241)

    print("[" + str(datetime.now()) + "] WordCloud Finished..")