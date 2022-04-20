from datetime import datetime
import pandas as pd
import random
import numpy as np
import math


def getCFRecommendation(userRatings):
    print("[" + str(datetime.now()) + "] CF Recomm Started..")

    # 0. Utility Matirix 로드와 사용자/영화 리스트를 추출한다.
    ### 0.1 user list를 로드한다.
    totalUserIDList = getTotalUserIDList("data/user_id_review_cnt_over10.csv")
    print("[" + str(datetime.now()) + "] Total {0} User IDs are loaded..".format(len(totalUserIDList)))

    ### 0.2 movie list를 로드한다.
    totalMovieIDList = getTotalMovieIDList("data/movie_id_year_11829.csv")
    print("[" + str(datetime.now()) + "] Total {0} Movie IDs are loaded..".format(len(totalMovieIDList)))

    ### 0.3 utility matrix를 생성한다.
    utilityMatrix_Dict, ratingCnt = getUtilityMatrix("data/review/", totalUserIDList, totalMovieIDList)
    print("[" + str(datetime.now()) + "] Total {0} Ratings are loaded as Utility Matrix..".format(ratingCnt))

    # 1. 유사 사용자를 찾는다.
    similarUserCnt = 10
    commonItemLimit = 5
    similarLimit = 0.4
    similarUserList = getSimilarUserList(userRatings, similarUserCnt, commonItemLimit, similarLimit, utilityMatrix_Dict)
    print("[" + str(datetime.now()) + "] Similar {0} Users are Extracted..".format(len(similarUserList)))

    # 2. 추천할 영화에 대해 유사 사용자의 점수를 이용하여, 타겟 사용자의 점수를 예측한다.
    viewLimit = 2
    recomMovieList = getRecommMovieList(similarUserList, utilityMatrix_Dict, viewLimit)
    print("[" + str(datetime.now()) + "] {0} Recommendation Candidates are Extracted....".format(len(recomMovieList)))

    # 3. 점수순으로 Top N개의 영화를 추출한다.
    finalTopN = 20
    finalRecommList = getTopRecommendation(recomMovieList, finalTopN)
    # print(finalRecommList)


    print("[" + str(datetime.now()) + "] CF Recomm Finished..")
    return finalRecommList




def getTopRecommendation(recomMovieList, finalTopN):
    recomMovieList.sort(key=lambda x: -x[1])
    return recomMovieList[:finalTopN]



def getRecommMovieList(similarUserList, utilityMatrix_Dict, viewLimit):
    finalList = []

    recomMovieDict = {}
    for simUserInfo in similarUserList:
        uID = simUserInfo[0]
        mDict = utilityMatrix_Dict[uID]

        mKeySet = mDict.keys()
        for mID in mKeySet:
            ratingVal = mDict[mID]

            if mID in recomMovieDict:
                recomMovieDict[mID].append(ratingVal)
            else:
                recomMovieDict[mID] = [ratingVal]

    recomMovieKeySet = recomMovieDict.keys()
    for recomMID in recomMovieKeySet:
        recomValList = recomMovieDict[recomMID]
        recomValList_Len = len(recomValList)
        if recomValList_Len >= viewLimit:
            cnt = 0
            sum = 0
            for val in recomValList:
                sum += val
                cnt += 1
            finalList.append([recomMID, sum/cnt])

    return finalList



def getSimilarUserList(userRatings, similarUserCnt, commonItemLimit, similarLimit, utilityMatrix_Dict):
    similarUserList = []

    userListKeySet = utilityMatrix_Dict.keys()
    for user in userListKeySet:
        simVal = getPCCVal(userRatings, utilityMatrix_Dict[user], commonItemLimit)
        if simVal >= similarLimit:
            similarUserList.append([user, simVal])

    similarUserList.sort(key=lambda x:-x[1])
    return similarUserList[:10]

# utilityMatrix_Dict = {}
# {
#     user234: {'39894':'5', '136315':'10'},
#     .....
#     user567, {'65432':'3', '67890':'7', '3643218':'8'}
# }

# [['39894', '5'], ['156464', '0'], ['136315', '10']]
def getPCCVal(userRatings_List, compareUserRatings_Dict, commonItemLimit):
    pccVal = 0

    commonCnt = 0

    xSum, ySum = 0, 0
    x2Sum, y2Sum = 0, 0
    xySum = 0
    for itemRating in userRatings_List:
        mID = int(itemRating[0])
        rating = int(itemRating[1])

        if mID in compareUserRatings_Dict:
            x = rating
            y = int(compareUserRatings_Dict[mID])

            xSum += x
            ySum += y
            x2Sum += (x*x)
            y2Sum += (y*y)
            xySum += (x*y)

            commonCnt += 1

    if (commonCnt >= commonItemLimit):
        up = (commonCnt * xySum) - (xSum*ySum)
        do = math.sqrt(commonCnt*x2Sum - (xSum*xSum)) * math.sqrt(commonCnt*y2Sum - (ySum*ySum))

        if do != 0:
            pccVal = up / do

    return pccVal



def getUtilityMatrix(reviewFilePath, userList, movieList):
    # utilityMatrix = np.full((len(userList), len(movieList)), 0, dtype=int)
    # print("[" + str(datetime.now()) + "] Utility Matrix" + str(utilityMatrix.shape) + " is Initialized..")

    utilityMatrix_Dict = {}
    for user in userList:
        utilityMatrix_Dict[user] = {}
    print("[" + str(datetime.now()) + "] Utility Matrix (Dict Type) is Initialized..")


    ratingCnt = 0
    reviewCnt = 0
    for i in range(2000, 2023):
        fileName = reviewFilePath + str(i) + "_review.csv"
        file_read = open(fileName, "r", encoding='UTF8')
        f_reader = pd.read_csv(file_read)
        f_reader_Arr = f_reader.to_numpy()
        for row in f_reader_Arr:
            uID = row[3]
            mID = row[0]
            rating = row[1]

            ## 1. uid, mid index를 찾아서, 값을 세팅 하는 방법
            # u_idxArr = np.where(userList == uID)[0]
            # m_idxArr = np.where(movieList == mID)[0]
            # if (len(u_idxArr) > 0) and (len(m_idxArr) > 0):
            #     ratingCnt += 1
            #     utilityMatrix[u_idxArr[0]][m_idxArr[0]] = int(rating)
            # >>>> 1만개 리뷰 처리 하는데 30초 소요 >> 전체 7시간 소요 예상 >> 적용 불가

            ## 2. utility matrix를 array가 아닌, Dictionary로 가져가는 방법
            try:
                utilityMatrix_Dict[uID][mID] = int(rating)
                ratingCnt += 1
            except Exception as e:
                # print(e)
                pass
            ## >>>> 50초에 로딩


            reviewCnt += 1
            # if ((reviewCnt%1000000)==0):
            #     print("[" + str(datetime.now()) + "] {0} reviews are loaded..".format(reviewCnt))

        file_read.close()

    # print("[" + str(datetime.now()) + "] Total {0} reviews are loaded..".format(reviewCnt))

    return utilityMatrix_Dict, ratingCnt

def getTotalMovieIDList(filePath):
    movieList = []
    file_read = open(filePath, "r", encoding='UTF8')

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    for row in f_reader_Arr:
        movieList.append(row[1])

    file_read.close()
    return np.array(movieList)

def getTotalUserIDList(filePath):
    userList = []
    file_read = open(filePath, "r", encoding='UTF8')

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    for row in f_reader_Arr:
        userList.append(row[0])

    file_read.close()
    return np.array(userList)




if __name__ == "__main__":
    print("[" + str(datetime.now()) + "] cfRecom Started..")

    tempUserRatingList = [['39894', '5'], ['156464', '0'], ['136315', '10'], ['167651', '8'], ['47385', '9'], ['44913', '6'], ['68555', '4'], ['83893', '7'], ['121048', '8'], ['185917', '9']]
    print("[" + str(datetime.now()) + "] User Rating Test >>")
    print(tempUserRatingList)

    recomMovieIDList = getCFRecommendation(tempUserRatingList)

    print("[" + str(datetime.now()) + "] cfRecom Results >>")
    print(recomMovieIDList)


    print("[" + str(datetime.now()) + "] cfRecom Finished..")

