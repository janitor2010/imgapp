import numpy as np
import cv2
import os
import sys
from flask import jsonify
from sklearn import preprocessing, model_selection, neighbors
# from sklearn.svm import SVC
# from sklearn.ensemble import RandomForestClassifier
#
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import pandas as pd
# from matplotlib import pyplot as plt
# import seaborn as sns
import pickle

#TODO: считать кол-во разных цветоа
class ImageDetection:
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(self.path)

    def main(self):
        pass

    @staticmethod
    def readImg(path):
        return cv2.imread(path)

    @staticmethod
    def predictSVM(img):

        df = ImageDetection.makeTestData(img)

        res = ImageDetection.makeClassifierSVM()
        clf, accuracy = res
        prediction = clf.predict(df)
        return prediction[0], accuracy

    @staticmethod
    def predictNeigbors(img):

        df = ImageDetection.makeTestDataTestFeatures(img)

        res = ImageDetection.makeClassifierNeigbors()
        clf, accuracy = res
        prediction = clf.predict(df)
        return prediction[0], accuracy

    @staticmethod
    def predictForest():

        df = ImageDetection.makeTestDataTestFeatures()

        res = ImageDetection.makeClassifierForest()
        clf, accuracy = res
        prediction = clf.predict(df)
        return prediction[0], accuracy

    @staticmethod
    def makeTestData(img):

        wPercent = ImageDetection.whitePercent(img)
        faces = ImageDetection.countFaces(img)
        objs = ImageDetection.findObjects(img)

        squares = objs['square'] if 'square' in objs else 0
        smalls = objs['small'] if 'small' in objs else 0
        rectangles = objs['rectangle'] if 'rectangle' in objs else 0
        triangles = objs['triangle'] if 'triangle' in objs else 0
        pentagons = objs['pentagon'] if 'pentagon' in objs else 0
        circles = objs['circle'] if 'circle' in objs else 0
        undefineds = objs['undefined'] if 'undefined' in objs else 0

        edges = ImageDetection.edgedImage(img)
        edgesPercent = ImageDetection.whitePercent(edges)

        df = pd.DataFrame(columns = ['Name','WhitePercent','Faces','Squares','Smalls','Rectangles','Triangles','Pentagons','Circles','Undefineds','EdgesPercent'])

        df = df.append({'Name':'6464','WhitePercent':wPercent,'Faces':faces,'Squares':squares,'Smalls':smalls,'Rectangles':rectangles,
        'Triangles':triangles,'Pentagons':pentagons,'Circles':circles,'Undefineds':undefineds,'EdgesPercent':edgesPercent}, ignore_index = True)

        return df

    @staticmethod
    def makeTestDataTestFeatures(img):

        wPercent = ImageDetection.whitePercent(img)

        faces = ImageDetection.countFaces(img)

        objs = ImageDetection.findObjects(img)


        #
        # squares = objs['square'] if 'square' in objs else 0
        smalls = objs['small'] if 'small' in objs else 0
        # rectangles = objs['rectangle'] if 'rectangle' in objs else 0
        # triangles = objs['triangle'] if 'triangle' in objs else 0
        # pentagons = objs['pentagon'] if 'pentagon' in objs else 0
        # circles = objs['circle'] if 'circle' in objs else 0
        undefineds = objs['undefined'] if 'undefined' in objs else 0


        edges = ImageDetection.edgedImage(img)

        edgesPercent = ImageDetection.whitePercent(edges)


        df = pd.DataFrame(columns = ['WhitePercent','Faces','Smalls','Undefineds','EdgesPercent'])

        df = df.append({'WhitePercent':wPercent,'Faces':faces,'EdgesPercent':edgesPercent,'Smalls':smalls,'Undefineds':undefineds}, ignore_index = True)

        return df

    @staticmethod
    def makeClassifierNeigbors():
        X_train, X_test, y_train, y_test = ImageDetection.makeTrainingGroupsSpecial()

        clf = neighbors.KNeighborsClassifier()

        clf, accuracy = ImageDetection.trainClassifier(clf, X_train, X_test, y_train, y_test)

        return clf, accuracy
        #
        # accuracy = clf.score(X_test, y_test)
        # print(accuracy)

    @staticmethod
    def makeClassifierForest():
        X_train, X_test, y_train, y_test = ImageDetection.makeTrainingGroupsSpecial()

        clf = RandomForestClassifier()

        clf, accuracy = ImageDetection.trainClassifier(clf, X_train, X_test, y_train, y_test)

        return clf, accuracy

    @staticmethod
    def makeTrainingGroups():
        df = pd.read_csv('all.csv')

        X = np.array(df.drop(['Value','Name'],1))
        X = preprocessing.scale(X)
        y = np.array(df['Value'])

        X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.2)

        return X_train, X_test, y_train, y_test

    @staticmethod
    def makeTrainingGroupsSpecial():
        df = pd.read_csv('two.csv')

        X = np.array(df.drop(['Value','Name','Squares','Smalls','Rectangles','Triangles','Pentagons','Circles','Undefineds'],1))

        X = preprocessing.scale(X)
        y = np.array(df['Value'])

        X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.2)

        return X_train, X_test, y_train, y_test

    @staticmethod
    def trainClassifier(clf, X_train, X_test, y_train, y_test):
        clf.fit(X_train, y_train)

        accuracy = clf.score(X_test, y_test)

        return clf, accuracy

    @staticmethod
    def makeClassifierSVM():
        X_train, X_test, y_train, y_test = ImageDetection.makeTrainingGroups()

        clf = SVC()

        clf, accuracy = ImageDetection.trainClassifier(clf, X_train, X_test, y_train, y_test)

        return clf, accuracy

    @staticmethod
    def show(img):
        # выводим картинку
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def whitePercent(img):
        # превращаем в грэйскэйл
        gray = ImageDetection.grayscaleImg(img)

        # оставляем только ч/б через пороговое значение
        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

        allPixels = thresh.size
        white = cv2.countNonZero(thresh)
        # black = thresh.size-white

        # процентное кол-во белого
        return white*100/allPixels

    @staticmethod
    def corneredImage(img):
        corners = cv2.goodFeaturesToTrack(img,25,0.01,10)
        corners = np.int0(corners)

        for i in corners:
            x,y = i.ravel()
            cv2.circle(img,(x,y),3,255,-1)

        return img

    @staticmethod
    def countFaces(img):

        gray = ImageDetection.grayscaleImg(img)
        print("here3")
        # слегка повышаем контрастность
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)





        # fileDir = os.path.dirname(os.path.realpath('__file__'))
        # filename = os.path.join(fileDir, 'backend/ImgApp/restart.txt')
        # fileP = os.path.join(fileDir, 'backend/ImgApp/')
        # sys.path.append(fileP)
        # print(os.path.dirname(__file__))
    #    print(fileP)
    #    return 3

    #    face_cascade = cv2.CascadeClassifier('/home/l/lubaberm/lubaberm.beget.tech/HelloFlask/haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(ImageDetection.filePath('haarcascade_frontalface_default.xml'))

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # for (x,y,w,h) in faces:
        #     img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #     roi_gray = gray[y:y+h, x:x+w]
        #     roi_color = img[y:y+h, x:x+w]
        #     eyes = eye_cascade.detectMultiScale(roi_gray)
        #     for (ex,ey,ew,eh) in eyes:
        #         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        return len(faces)

    @staticmethod
    def edgedImage(img):

        gray = ImageDetection.grayscaleImg(img)

        edges = cv2.Canny(gray,100,200)
        return edges

    @staticmethod
    def grayscaleImg(img):
        if not ImageDetection.isGray(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        return gray

    @staticmethod
    def detectShape(c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        #пропускаем слишком маленькие формы
        if (peri < 200): return "small"

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

            # if the shape has 4 vertices, it is either a square or
            # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"



            # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

            # otherwise, we assume the shape is a circle
        elif len(approx) <= 1:
            shape = "circle"
        else:
            shape = "undefined"



            # return the name of the shape
        return shape

    @staticmethod
    def findObjects(img):

        height, width = img.shape[:2]
        heightMult = height/width
    #    resized = imageInitial
        resized = cv2.resize(img,(300, int(300*heightMult)), interpolation = cv2.INTER_CUBIC)
        ratio = img.shape[0] / float(resized.shape[0])



        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        image, contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # можем нарисовать контур на изначальном изображении
        # img = cv2.drawContours(resized, contours, -1, (0,255,0), 3)

        arr = {}

        # loop over the contours
        for c in contours:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            # M = cv2.moments(c)
            # cX = int((M["m10"] / M["m00"]) * ratio)
            # cY = int((M["m01"] / M["m00"]) * ratio)
            shape = ImageDetection.detectShape(c)
            if shape in arr:
                arr[shape] += 1
            else:
                arr[shape] = 1


        return arr

    @staticmethod
    def isGray(img):
        return False if len(img.shape)==3 else True

    @staticmethod
    def saveToCSV():
        folders = os.listdir('i')

        scope = []

        for cl in folders:
            imagesGroup = {}
            imagesGroup[cl] = os.listdir('i/'+cl)
            scope.append(imagesGroup)

        df = pd.DataFrame(columns = ['WhitePercent','Faces','Squares','Smalls','Rectangles','Triangles','Pentagons','Circles','Undefineds','EdgesPercent','Value'])

        for imgGroup in scope:
            for groupName, imgArr in imgGroup.items():
                for i in imgArr:
                    img = cv2.imread('i/'+groupName+'/'+i)

                    wPercent = ImageDetection.whitePercent(img)
                    faces = ImageDetection.countFaces(img)
                    objs = ImageDetection.findObjects(img)

                    squares = objs['square'] if 'square' in objs else 0
                    smalls = objs['small'] if 'small' in objs else 0
                    rectangles = objs['rectangle'] if 'rectangle' in objs else 0
                    triangles = objs['triangle'] if 'triangle' in objs else 0
                    pentagons = objs['pentagon'] if 'pentagon' in objs else 0
                    circles = objs['circle'] if 'circle' in objs else 0
                    undefineds = objs['undefined'] if 'undefined' in objs else 0

                    edges = ImageDetection.edgedImage(img)
                    edgesPercent = ImageDetection.whitePercent(edges)

                    df = df.append({'WhitePercent':wPercent,'Faces':faces,'Squares':squares,'Smalls':smalls,'Rectangles':rectangles,
                    'Triangles':triangles,'Pentagons':pentagons,'Circles':circles,'Undefineds':undefineds,'EdgesPercent':edgesPercent,'Value':groupName}, ignore_index = True)


        df.to_csv('all.csv', index=False)

    def saveToCSVOnlyTwo(self):
        folders = os.listdir('i')

        scope = []

        for cl in folders:
            imagesGroup = {}
            if cl=='abstract':
                continue
            imagesGroup[cl] = os.listdir('i/'+cl)
            scope.append(imagesGroup)

        df = pd.DataFrame(columns = ['Name','WhitePercent','Faces','Squares','Smalls','Rectangles','Triangles','Pentagons','Circles','Undefineds','EdgesPercent','Value'])

        for imgGroup in scope:
            for groupName, imgArr in imgGroup.items():
                for i in imgArr:
                    img = cv2.imread('i/'+groupName+'/'+i)

                    wPercent = self.whitePercent()
                    faces = self.countFaces()
                    objs = self.findObjects()

                    squares = objs['square'] if 'square' in objs else 0
                    smalls = objs['small'] if 'small' in objs else 0
                    rectangles = objs['rectangle'] if 'rectangle' in objs else 0
                    triangles = objs['triangle'] if 'triangle' in objs else 0
                    pentagons = objs['pentagon'] if 'pentagon' in objs else 0
                    circles = objs['circle'] if 'circle' in objs else 0
                    undefineds = objs['undefined'] if 'undefined' in objs else 0

                    edges = self.edgedImage(img)
                    edgesPercent = self.whitePercent(edges)

                    df = df.append({'Name':i,'WhitePercent':wPercent,'Faces':faces,'Squares':squares,'Smalls':smalls,'Rectangles':rectangles,
                    'Triangles':triangles,'Pentagons':pentagons,'Circles':circles,'Undefineds':undefineds,'EdgesPercent':edgesPercent,'Value':groupName}, ignore_index = True)


        df.to_csv('two.csv')

    @staticmethod
    def mmain(path):
        im = ImageDetection.readImg(path)
        testOne = ImageDetection.makeTestDataTestFeatures(im)

        df = pd.read_csv('all.csv')

        labelEncoder = preprocessing.LabelEncoder()
        for col in df.columns:
            if col != "Value":
                continue
            df[col] = labelEncoder.fit_transform(df[col])

        classes = labelEncoder.classes_

        X = df.drop(['Value','Squares','Rectangles','Triangles','Pentagons','Circles'],1)
        #X = preprocessing.scale(X)
        y = df['Value']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

        predicts = []
        keys = []
        scores = []
        models = {
        'Logistic Regression': LogisticRegression()
        # 'Decision Tree': DecisionTreeClassifier(),
        #           'Random Forest': RandomForestClassifier(n_estimators=30),
        #           'K-Nearest Neighbors':KNeighborsClassifier(n_neighbors=4),
        #             'Linear SVM':SVC(kernel='rbf', gamma=.10, C=1.0)
                    }

        for k,v in models.items():
            mod = v
            mod.fit(X_train, y_train)

            # with open('data.pickleMod', 'wb') as f:
            #     pickle.dump(mod, f)

            with open('data.pickleMod', 'rb') as f:
                mod = pickle.load(f)

            pred = mod.predict(X_test)
            # print('Results for: ' + str(k) + '\n')
            # print(confusion_matrix(y_test, pred))
            # print(classification_report(y_test, pred))
            acc = accuracy_score(y_test, pred)
            # print(acc)
            # print('\n' + '\n')
            predTester = mod.predict(testOne)
            # print('Results for TESTER: ' + '\n')
            # # print(confusion_matrix(testOne, predTester))
            # print(testOne)
            # print(predTester)
            # print(classification_report(testOne, predTester[0]))
            # # acc2 = accuracy_score(testOne, predTester)
            # # print(acc2)
            # print(testOne)
            # print(predTester)
            # print('\n' + '\n')

            predicts.append(classes[predTester[0]])
            keys.append(k)
            scores.append(acc)
            table = pd.DataFrame({'model':keys, 'accuracy score':scores, 'prediction': predicts})

        return table

    @staticmethod
    def mmainLight(img):
    #    im = ImageDetection.readImg(path)
        print("here")
        testOne = ImageDetection.makeTestDataTestFeatures(img)
        print(testOne)


    #    with open('/home/l/lubaberm/lubaberm.beget.tech/HelloFlask/data.pickleMod', 'rb') as f:
        with open(ImageDetection.filePath('data.pickleMod'), 'rb') as f:
            mod = pickle.load(f)

        # return "hhhhhhh123"
        # pred = mod.predict(X_test)
        # # print('Results for: ' + str(k) + '\n')
        # # print(confusion_matrix(y_test, pred))
        # # print(classification_report(y_test, pred))
        # acc = accuracy_score(y_test, pred)
        # print(acc)
        # print('\n' + '\n')
        predTester = mod.predict(testOne)
        # print('Results for TESTER: ' + '\n')
        # # print(confusion_matrix(testOne, predTester))
        # print(testOne)
        # print(predTester)
        # print(classification_report(testOne, predTester[0]))
        # # acc2 = accuracy_score(testOne, predTester)
        # # print(acc2)
        # print(testOne)
        # print(predTester)
        # print('\n' + '\n')

        # predicts.append(classes[predTester[0]])
        # keys.append(k)
        # scores.append(acc)
        # table = pd.DataFrame({'model':keys, 'accuracy score':scores, 'prediction': predicts})
        infs = {}
        infs['white'] = np.array(testOne['WhitePercent'])[0]
        infs['faces'] = np.array(testOne['Faces'])[0]
        infs['edges'] = np.array(testOne['EdgesPercent'])[0]
        infs['smalls'] = np.array(testOne['Smalls'])[0]
        print(infs)

        return predTester, infs

    @staticmethod
    def filePath(path):
        # ищет всегда путь к файлу относительно пути, где был запущен скрипт. Здесь ищем текущую папку и находим нужный файл в ней
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        return os.path.join(__location__, path)

    @staticmethod
    def manualLogging(filename):
        # создаем в текущей папке файл
        path1 = ImageDetection.filePath(filename)
        file1 = open(path1,'w')
        file1.write('Hello World')
        file1.close()
