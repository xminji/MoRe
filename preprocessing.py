from datetime import datetime
import csv
import pandas as pd
import numpy as np

def start():
    # 리뷰 내 사용자 수
    # 사용자당 평균 리뷰 수 & 표준편차
    # getUserReviewCnt()
    print("[" + str(datetime.now()) + "] getUserReviewCnt() finished..")

    # 수집된 영화 내 포함된 unique 장르 목록, 각 장르별 영화 수
    # getMovieGenreAndCnt()
    print("[" + str(datetime.now()) + "] getMovieGenreAndCnt() finished..")

    attachYearToMovie()

def attachYearToMovie():
    file_read = open("data/movie_id_top50(review_cnt).csv", "r")

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    w_List = []

    for row in f_reader_Arr:
        mID = row[2]

        for i in range(2000, 2023):
            fileName = "data/movie/" + str(i) + ".csv"
            yFile_read = open(fileName, "r")
            y_reader = pd.read_csv(yFile_read, sep='\t')

            y_readerList = list(y_reader.code)
            if mID in y_readerList:
                w_List.append((mID, i))
                yFile_read.close()
                break
            else:
                yFile_read.close()

    file_read.close()

    print(w_List)








    file_read.close()


def getMovieGenreAndCnt():

    targetMovieIDList = getTargetMovieList("data/movie_id_11829.csv")
    #
    # genreCntDict = {}
    # readCnt = 0
    # for i in range(2000, 2023):
    #     fileName = "data/movie/" + str(i) + ".csv"
    #     file_read = open(fileName, "r")
    #
    #     f_reader = pd.read_csv(file_read, sep='\t')
    #     f_reader_Arr = f_reader.to_numpy()
    #
    #     for row in f_reader_Arr:
    #         readCnt = readCnt + 1
    #
    #         if row[1] not in targetMovieIDList:
    #             continue
    #         if str(type(row[3])) == "<class 'float'>":
    #             continue
    #
    #         genreArr = row[3].split(',')
    #         for genre in genreArr:
    #             g = genre.strip()
    #             if g in genreCntDict:
    #                 genreCntDict[g] = genreCntDict[g] + 1
    #             else:
    #                 genreCntDict[g] = 1
    #
    #     file_read.close()
    #     print("[" + str(datetime.now()) + "] '{0}' file is processed..".format(fileName))
    #
    # print("[" + str(datetime.now()) + "] All files are processed..")
    # print("[" + str(datetime.now()) + "] Total Movie Count: {0}..".format(readCnt))
    #
    # print(genreCntDict.keys())
    # print(genreCntDict)


def getTargetMovieList(fileName):
    movieIDList = []

    file_read = open(fileName, "r")

    f_reader = pd.read_csv(file_read)
    f_reader_Arr = f_reader.to_numpy()

    for row in f_reader_Arr:
        movieIDList.append(row[1])

    file_read.close()


    return movieIDList


def getUserReviewCnt():
    # 전체 unique 사용자와 사용자당 리뷰수를 카운트 한 후
    # 카운트에 대한 편균/표준편차 및 4분위수 추출

    userReviewCntDict = {}

    ## 리뷰 파일로부터 unique 사용자 기준, 사용자별 리뷰 수 딕셔너리 생성
    # readCnt = 0
    # for i in range(2000, 2023):
    #     fileName = "data/review/" + str(i) + "_review.csv"
    #     file_read = open(fileName, "r")
    #
    #     f_reader = pd.read_csv(file_read)
    #     f_reader_Arr = f_reader.to_numpy()
    #
    #     for row in f_reader_Arr:
    #         readCnt = readCnt + 1
    #
    #         userID = row[3]
    #         if userID in userReviewCntDict:
    #             # print(userID)
    #             userReviewCntDict[userID] = userReviewCntDict[userID] + 1
    #         else:
    #             userReviewCntDict[userID] = 1
    #
    #     file_read.close()
    #     print("[" + str(datetime.now()) + "] '{0}' file is processed..".format(fileName))
    #
    # print("[" + str(datetime.now()) + "] All files are processed..")
    # print("[" + str(datetime.now()) + "] Total Review Count: {0}..".format(readCnt))
    # print("Total Unique User Cnt: {0}".format(len(userReviewCntDict)))

    ## 사용자별 리뷰 수 딕셔너리에 대한 파일 생성 (최소 리뷰 개수 적용)
    # limit = 10
    # file_write = open("data/user_id_review_cnt_over{0}.csv".format(limit), "w")
    # for k in userReviewCntDict.keys():
    #     v = userReviewCntDict[k]
    #     if v >= limit:
    #         file_write.write("{0},{1}\n".format(k, v))
    # file_write.close()
    # print("[" + str(datetime.now()) + "] User ID & Review_Cnt are written..")

    ## 사용자별 리뷰 수 딕셔너리 정보를 기 생성된 파일로부터 로딩
    # file_read = open("data/user_id_review_cnt_over10.csv", "r")
    # f_reader = csv.reader(file_read)
    # for line in f_reader:
    #     userReviewCntDict[line[0]] = line[1]
    # file_read.close()

    print("Total Unique User Cnt: {0}".format(len(userReviewCntDict)))

    ## 딕셔너리에서 리뷰 카운트만 배열로 불러온 후, 배열 계산 기능 이용
    # reviewCntArr_str = list(userReviewCntDict.values())
    # reviewCntArr = list(map(int, reviewCntArr_str))
    #
    # print("min> ", min(reviewCntArr))
    # print("max> ", max(reviewCntArr))
    # print("avg> ", np.mean(reviewCntArr))
    #
    # arr_pd = pd.Series(reviewCntArr)
    # print("Q1> ", arr_pd.quantile(.25))
    # print("Q2> ", arr_pd.quantile(.5))
    # print("Q3> ", arr_pd.quantile(.75))







###########################################################
# main execution
if __name__ == "__main__":
    print("[" + str(datetime.now()) + "] preprocessing Started..")

    start()

    print("[" + str(datetime.now()) + "] preprocessing Finished..")