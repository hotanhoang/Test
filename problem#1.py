'''
    Sau khi tìm hiểu yêu câu bài toán, tôi tiến hành phân tích như sau:
        1.  Thang máy có thể đi lên hoặc đi xuống và sẽ dừng lại ở tầng mà người sử dụng yêu cầu.
        2.  Nếu thang máy nhận dược yêu câuf đi xuống trong khi đang đi lên thì nó sẽ đi lên tầng cao nhất đối với yêu cầu hiện tai rồi mới đi xuống
        3.  Người sử dụng có thể gửi request bất kì lúc nào.
        4.  Thang máy hoạt động sẽ ưu tiên về khoảng cách thay vì thời gian. C ónghĩa là, giả sử nếu thang máy đang ở tầng 1, người A muốn đi lên tầng 4,
        sau đo người B nhấn nút để đi lên tầng 2. Tuy người A yêu cầu thang máy trước nhưng thang máy sẽ không đi lên tầng 4 rồi xuống lại tầng 2 mà sẽ dùng
        lại ở tầng 2 để người B ra ngoài sau đó đi lên tầng 4. Do đó, yêu cầu sẽ được sắp xếp theo khoảng cách thay vì sắp xếp theo thời gian.
    ý tưởng:
        ở đây tôi giả sử là yêu cầu đi lên sẽ được ưu tiên hơn yêu cầu thi xuống. Điều đó có nghĩa rằng khi thang máy đang ở tình trạng chờ, 
        nếu cả 2 đi lên và đi xuống được yêu cầu cùng lúc thì yêu cầu đi lên sẽ được ưu tiên hơn.
        Sử dụng OOP để giải quyết bài toán:
            1.  Thiết kết lớp Resquest, lớp Elevator để đại diện cho các instance trong thực tế.
            2.  Sử dụng cấu trúc dữ liệu hàng đợi ưu tiên (PriorityQueue) để lưu và sử lý các request vì ở đây ưu tiên theo khoảng cách
            3.  Sử dụng priorityQueue để lưu các yêu cầu đi xuống và sắp xếp chúng dựa theo desired floor. Tương tự, tôi cũng sử dụng priorityQueue để lưu các yêu
            đi lên và sắp xếp theo disired floor
            4. Khi mà người sử dụng thang máy yêu cầu ở bên ngoài thì thang máy dừng lại tại tầng hiện tại của người gửi yêu cầu để pickup người đó vào thang máy trước
            khi tiếp tục đi đến desired floor
        UP: đi lên
        DOWN: đi xuông
        IDLE: trạng thái chờ
        IN: trong thang máy
        OUT: ngoài thang máy
'''


from queue import PriorityQueue
class Resquest():
    def __init__(self,currentFLoor, desiredFloor, direction, location):
        self.currentFloor = currentFLoor
        self.desiredFloor = desiredFloor
        self.direction = direction
        self.location = location

    #chinh sua ham so sanh cua hang doi uu tien
    def __lt__(self, other):
        return self.desiredFloor - other.desiredFloor

class Elevator():
    def __init__(self, currentFloor):
        self.upQueue = PriorityQueue()
        self.downQueue = PriorityQueue()
        self.currentFLoor = currentFloor
        #Khởi tạo trang thái ban đầu là
        self.directon = 'IDLE'


    def sendUpResquest(self, upRequest):
        '''
            Nếu như yêu cầu được gửi từ bên ngoài của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired
        '''
        if(upRequest.location == 'OUTSIDE'):
            req = Resquest(upRequest.currentFloor, upRequest.currentFloor, 'UP', 'OUT')
            self.upQueue.put(req)
            print('Them 1 yeu cau di len tai tang: ' + str(upRequest.currentFloor))
        '''
            Nếu như yêu cầu được gửi từ bên trong của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired
        '''
        req = Resquest(upRequest.currentFloor, upRequest.currentFloor, 'UP', 'IN')
        self.upQueue.put(req)
        print('Them 1 yeu cau di len tai tang: ' + str(upRequest.currentFloor))

    def sendDownResquest(self, downRequest):
        '''
        Nếu như yêu cầu được gửi từ bên ngoài của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired floor
        '''
        if(downRequest.location == 'OUTSIDE'):
            req = Resquest(downRequest.currentFloor, downRequest.currentFloor, 'DOWN', 'OUT')
            self.upQueue.put(req)
            print('Them 1 yeu cau di xuong tai tang: ' + str(downRequest.currentFloor))
        '''
            Nếu như yêu cầu được gửi từ bên trong của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired floor
        '''
        req = Resquest(downRequest.currentFloor, downRequest.currentFloor, 'DOWN', 'IN')
        self.upQueue.put(req)
        print('Them 1 yeu cau di xuong  tai tang: ' + str(downRequest.currentFloor))

    def processUpResquest(self):
        while(not self.upQueue.empty()):
            upResquest = self.upQueue.get()
            self.currentFLoor = upResquest.desiredFloor
            print('Thang may dung lai tai tang ' + str(self.currentFLoor))
        if(not self.downQueue.empty()):
            self.directon = 'DOWN'
        else:
            self.directon = 'IDLE'
    def processDownResquest(self):
        while(not self.downQueue.empty()):
            downResquest = self.upQueue.get()
            self.currentFLoor = downResquest.desiredFloor
            print('Thang may dung lai tai tang ' + str(self.currentFLoor))
        if(not self.downQueue.empty()):
            self.directon = 'UP'
        else:
            self.directon = 'IDLE'
    def processResquest(self):
        if(self.directon == 'UP' or self.directon == 'IDLE'):
            self.processUpResquest()
            self.processDownResquest()
        else:
            self.processDownResquest()
            self.processUpResquest()
    def main(self):
        while(not self.upQueue.empty() or not self.downQueue.empty()):
            self.processResquest()
        print('Tien trinh ket thuc!!!!!!')
        self.directon = 'IDLE'
if __name__ == '__main__':
    elevator = Elevator(0)
    requestUp_1 = Resquest(elevator.currentFLoor, 5, 'UP', 'IN')
    requestUp_2 = Resquest(elevator.currentFLoor, 3, 'UP', 'IN')

    requestDown_1 = Resquest(elevator.currentFLoor, 1, 'DOWN', 'IN')
    requestDown_2 = Resquest(elevator.currentFLoor, 2, 'DOWN', 'IN')
    requestDown_3 = Resquest(4, 0, 'DOWN', 'OUT')

    #Giả sử có 2 người ở trong thang máy thực hiện 2 yêu cầu requestUp_1à và RequestUp_2
    elevator.sendUpResquest(upRequest=requestUp_1)
    elevator.sendUpResquest(upRequest=requestUp_2)

    #Giả sử 1 người ở bên ngoài tầng 4 thực hiên yêu cầu requestDown_3
    elevator.sendDownResquest(downRequest=requestDown_3)

    #Giả sử 2 người ở bên trong thang m áythực hiên 2 yêu cầu requestDown_1 v requestDown_2
    elevator.sendDownResquest(downRequest=requestDown_1)
    elevator.sendDownResquest(downRequest=requestDown_2)


