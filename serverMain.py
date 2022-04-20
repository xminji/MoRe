from datetime import datetime
from flask import Flask, render_template, request
import pandas as pd
import random
import cfRecom, genreRecom
import analysis
import re
app = Flask(__name__, template_folder='templates')



@app.after_request
def set_response_headers(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    return r


#############################################################
# index 영역 / 초기에 점수를 입력하도록 할 영화를 보여준다.
#############################################################
@app.route('/')
def mainResponse():
    print("[" + str(datetime.now()) + "] Server Request Income: '/'")

    movieInfoList = getInitialMovieInfo(10)

    return render_template('index.html', movieInfoList=movieInfoList)


#############################################################
# 초기 인덱스 화면에서 보여줄 영화를 랜덤으로 추출하고,
# 해당 영화의 정보를 가져온다.
#############################################################
def getInitialMovieInfo(getCnt):
    movieInfoDictList = []
    # movieInfoDict.append(['movie1_name', 'movie1_year'])
    # movieInfoDict.append(['movie2_name', 'movie2_year'])

    file_read = open("data/movieIdTop50_year.csv", "r", encoding='UTF8')

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    initilList = []
    for row in f_reader_Arr:
        initilList.append([row[1], row[2]])

    file_read.close()

    random.shuffle(initilList)
    finalList = initilList[0:getCnt]

    for movie in finalList:
        # movieInfoFilePath = "data/movie/{0}.csv".format(movie[1])
        movieInfoDict = searchMovie(movie[1], movie[0])
        imgPath = "static/images/movie_top50/{0}.png".format(movie[0])

        mInfo = {"id":movie[0], "title":movieInfoDict['title'], "genre":movieInfoDict['genre'], "actor":movieInfoDict['actors'], "img":imgPath}
        movieInfoDictList.append(mInfo)
    return movieInfoDictList

#############################################################
# 추천 결과를 받아서, 결과내에 있는 영화들의 정보를 불러 온 후, HTML로 보여준다
#############################################################

@app.route('/result', methods=['GET', 'POST'])
def searchResponse():
    print("[" + str(datetime.now()) + "] Server Request Income: '/result'")

    userRatings = []
    userGenre = []
    userMbti = []
    if request.method == 'POST':
        formKeyList = request.form.keys()
        # print('formKeyList',formKeyList)
        for formKey in formKeyList:
            # index.html에서 genre 체크박스에서 체크된 값 저장
            if formKey == "genre":
                uGenre = request.form.getlist("genre")
                for glist in uGenre:
                    userGenre.append(glist)

            # index.html에서 mbti radio에서 체크된 값 저장
            if formKey == 'mbti':
                mbti = request.form[formKey]
                userMbti.append(mbti)

            # index.html에서 영화 점수 값 저장
            if formKey[0:7] == "rating_":
                mId = formKey[7:]
                rVal = request.form[formKey]
                userRatings.append([mId, rVal])



    # print(userRatings)

    ####################################################
    # TODO - recomMovieInfoList
    mbtiRecomList,genreRecomList = genreRecom.mbtiGenreRecomendation(userGenre, userMbti)
    #cfRecomList = [[31726, 10.0], [41375, 10.0], [38766, 10.0], [47385, 10.0], [73372, 10.0], [94775, 10.0], [47370, 10.0], [97857, 10.0], [45290, 10.0], [99740, 10.0], [82473, 10.0], [136898, 10.0], [174805, 10.0], [151153, 10.0], [184517, 10.0], [28788, 10.0], [34819, 10.0], [36344, 10.0], [38572, 10.0], [38464, 10.0]]
    cfRecomList = cfRecom.getCFRecommendation(userRatings)


    mbtiRecomInfoDictList = getMovieInfo(mbtiRecomList)
    genreRecomInfoDictList = getMovieInfo(genreRecomList)
    cfRecomInfoDictList = getMovieInfo(cfRecomList)


    cfRecomUnitKorList = []
    cfRecomUnitForList = []
    for i in range(len(cfRecomInfoDictList)):
        if cfRecomInfoDictList[i]['nation'] == '한국':
            cfRecomUnitKorList.append(cfRecomInfoDictList[i])
        else:
            cfRecomUnitForList.append(cfRecomInfoDictList[i])
    cfRecomInfoDictList_KOR = cfRecomUnitKorList
    cfRecomInfoDictList_FOR = cfRecomUnitForList


    return render_template('result.html', mbtiRecomInfoDictList=mbtiRecomInfoDictList, genreRecomInfoDictList=genreRecomInfoDictList, cfRecomInfoDictList_KOR=cfRecomInfoDictList_KOR, cfRecomInfoDictList_FOR=cfRecomInfoDictList_FOR)

def getMovieInfo(movieList):
    finalInfoDictList = []

    if len(movieList) > 0:
        for movie in movieList:
            mYear = getYearOfMovieID(movie[0])
            mInfoDict = searchMovie(mYear, movie[0])
            mInfoDict['year'] = mYear
            mInfoDict['id'] = movie[0]
            mInfoDict['rating'] = movie[1]
            finalInfoDictList.append(mInfoDict)


    return finalInfoDictList

# 리뷰가 있는 모든 영화 리스트에서 선택된 갯수만큼 랜덤 반환
def getInitialAllMovieInfo(getCnt):
    allMovieInfoDict = []

    file_read = open("data/movie_id_year_11829.csv", "r", encoding='UTF8')

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    initilList = []
    for row in f_reader_Arr:
        initilList.append([row[0], row[1]])

    file_read.close()

    random.shuffle(initilList)
    finalList = initilList[0:getCnt]

    for movie in finalList:
        movieInfoFilePath = "data/movie/{0}.csv".format(movie[0])
        movieInfoDict = searchMovie(movie[0], movie[1])


        mInfo = {"Year": movie[0], "id": movie[1], "title": movieInfoDict['title'], "genre": movieInfoDict['genre'], "actor": movieInfoDict['actors'], "img": movieInfoDict['img']}
        allMovieInfoDict.append( mInfo )

    return allMovieInfoDict


#############################################################
# 특정 영화 클릭시, 상세 정보를 보여준다
#############################################################

@app.route('/movieDetail', methods=['GET', 'POST'])
def viewMovieDetail():
    print("[" + str(datetime.now()) + "] Server Request Income: '/movieDetail'")


    if request.method == 'GET':
        mYear = request.args.get('year',"0",str)
        mId = request.args.get('id', "0", str)

        movieDetail = searchMovie(mYear,mId)

        # TODO
        wordCloudImgPath_po,wordCloudImgPath_ne = analysis.getWordCloudImg(mYear,mId)




    return render_template('movieDetail.html', movieDetail=movieDetail, wordCloudImgPath_po=wordCloudImgPath_po, wordCloudImgPath_ne=wordCloudImgPath_ne)

#############################################################
# 공통 영역 / movie 검색 후 영화 디테일 정보 반환
#############################################################
def searchMovie(mYear, mId):
    f_reader = pd.read_csv("data/movie/" + str(mYear) + ".csv",sep='\t')

    mTitle = ""
    mGenre = ""
    mNation = ""
    mRunningTime = ""
    mAge = ""
    mOpenDate = ""
    mActors = ""
    mStory = ""

    for num in range(len(f_reader)):
        if str(f_reader.code[num]) == str(mId):
            mTitle = f_reader.title[num]
            mGenre = f_reader.genre[num]
            mNation = f_reader.nation[num]
            mRunningTime = f_reader.runningTime[num]
            mOpenDate = f_reader.openDate[num]
            mActors = f_reader.actors[num]
            mStory = cleanText(str( f_reader.story[num]))

    imgPath = "static/images/allMovieImg/{0}/{1}.png".format(mYear, mId)

    movieinfo = {'title':mTitle, 'genre': mGenre, 'nation':mNation, 'runtime':mRunningTime, 'age':mAge, 'openDate':mOpenDate, 'actors':mActors, 'story':mStory, 'img':imgPath}

    return movieinfo



def getYearOfMovieID(mID):
    file_read = open("data/movie_id_year_11829.csv", "r", encoding='UTF8')

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    for row in f_reader_Arr:
        if mID == row[1]:
            return row[0]

    return -1

def cleanText(story_txt):
    cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') #정규표현 패턴의 메소드를 컴파일하여 cleaner에 매치
    text = re.sub(cleaner, '', str(story_txt)) #re.sub（정규 표현식, 대상 문자열 , 치환 문자）
    non_string = ['/', ':', '*', '{', '}', '|']  # 경로 금지 문자열 제거
    for str_ in non_string:
        if str_ in text:
            text = text.replace(str_, "")
    return text


##########################################
# Main Method
##########################################
if __name__ == "__main__":
    print("[" + str(datetime.now()) + "] Web Server Prepare..")
    app.run(host="127.0.0.1", port="8080")


    print("[" + str(datetime.now()) + "] Web Server is Stopped..")





