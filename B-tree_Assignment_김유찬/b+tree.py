import csv
import os
import sys
import pickle
import math
from collections import deque

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.leftchild = None
        self.rightchild = None
    # internal 노드 리스트에서 원하는 key의 인덱스 반환
    def find_my_key_in_internal(self, key):
        # self에 노드를 넘겨줘서 자기 자신 internal node 표현
        internal_nodelist = self.leftchild.parent
        index = 0
        for i in range(len(internal_nodelist.nodelist)):
            if internal_nodelist.nodelist[i].key == key:
                index = i
                # print("internal node에서 인덱스" + str(index))
                break
        return index
    
    def __repr__(self):
        return f"Node(key={self.key}, value={self.value})"

class NodeList:
    def __init__(self, size, file):
        self.head = None
        self.parent = None
        self.isleaf = True
        self.size = size
        self.file = file
        self.nodelist = []
        self.next = None # 리프 노드일 때 다음 노드리스트 가리킴

    #삽입할 노드 리스트를 찾는 함수
    def find_position(self, key):
        current = self
        if current.isleaf:
            return current
        
        for i in range(len(current.nodelist)):
            # 왼쪽 자식으로 이동
            if key < current.nodelist[i].key:
                current = current.nodelist[i].leftchild
                break
            # 맨 마지막이면 오른쪽 자식으로 이동
            elif i == len(current.nodelist) - 1:
                current = current.nodelist[i].rightchild
            # 다음 노드로 이동
            else:
                continue
        # 자식 노드에서 다시 위치 찾기
        return current.find_position(key)
    
    # 부모의 자식들 재조정
    def rearrange(self):
        for i in range(len(self.nodelist) - 1):
            self.nodelist[i+1].leftchild = self.nodelist[i].rightchild
        

    # 분리하는 함수
    def split(self, fnodelist):
        # 부모가 없다면 새로운 부모 노드 리스트 생성
        if fnodelist.parent is None:
            parentnodelist = NodeList(self.size, self.file)
            parentnodelist.isleaf = False
            self.head = parentnodelist # 트리의 루트 바꿔주기
        # 부모가 있다면 그거 가져오기
        else:
            parentnodelist = fnodelist.parent            
        # 리프 노드 리스트를 분리할 때
        if fnodelist.isleaf:
            newnodelist = NodeList(self.size, self.file)
            split_point = int(self.size) // 2
            # 슬라이싱을 사용해 절반 분리
            newnodelist.nodelist = fnodelist.nodelist[split_point:]
            fnodelist.nodelist = fnodelist.nodelist[:split_point]
            # 리프 노드 리스트끼리 연결
            if fnodelist.next:
                newnodelist.next = fnodelist.next
                fnodelist.next = newnodelist
            else:
                fnodelist.next = newnodelist
            # 중간 값을 부모로 올림
            mid = newnodelist.nodelist[0]
            # print("중간 키 : " + str(mid.key))
            mid.leftchild = fnodelist
            mid.rightchild = newnodelist
            fnodelist.parent = parentnodelist
            newnodelist.parent = parentnodelist
            # parentnodelist에 mid 삽입
            self.insert(parentnodelist, mid)
        # 부모 노드 리스트를 분리할 때
        else:
            newnodelist = NodeList(self.size, self.file)
            newnodelist.isleaf = False
            split_point = int(self.size) // 2 + 1
            # 부모를 가리키는 변수 재조정
            for i in range(split_point - 1, len(fnodelist.nodelist)):
                fnodelist.nodelist[i].rightchild.parent = newnodelist
            # 슬라이싱을 사용해 절반 분리
            newnodelist.nodelist = fnodelist.nodelist[split_point:]
            fnodelist.nodelist = fnodelist.nodelist[:split_point]
            mid = fnodelist.nodelist.pop()
            # 중간값을 없애고 부모로 올림
            mid.leftchild = fnodelist
            mid.rightchild = newnodelist
            fnodelist.parent = parentnodelist
            newnodelist.parent = parentnodelist
            # parentnodelist에 mid 삽입
            self.insert(parentnodelist, mid)

    # 삽입 함수
    def insert(self, fnodelist, node):
        # 리프 노드 리스트에 넣고 오름차순 정렬
        fnodelist.nodelist.append(node)
        fnodelist.nodelist.sort(key = lambda x : x.key)
        if not fnodelist.isleaf:
            fnodelist.rearrange()
        # key가 size만큼 있으면 분리해야함
        if len(fnodelist.nodelist) == int(fnodelist.size): 
            self.split(fnodelist)

    # bptree를 파일에 쓰기
    def write_bptree_to_file(self, ifile):
        size = 1
        new_size = 0
        dq = deque()
        dq.append(self)
        with open(ifile, 'r') as file:
            node_size = file.readline()
        with open(ifile, 'w') as file:
            file.write(node_size + '\n')
            # BFS 방식으로 트리 순회
            while dq:
                for i in range(size):
                    current = dq.popleft()
                    # 노드의 key 기록
                    for j in range(len(current.nodelist)):
                        file.write(str(current.nodelist[j].key) + ' ')
                        # 자식 노드를 큐에 추가(리프 노드일 때는 추가하지 않음)
                        if not current.isleaf:
                            if current.nodelist[j].leftchild:
                                dq.append(current.nodelist[j].leftchild)
                                new_size += 1
                            if j == len(current.nodelist) - 1 and current.nodelist[j].rightchild:
                                dq.append(current.nodelist[j].rightchild)
                                new_size += 1
                    file.write(' | ')
                file.write('\n')
                size = new_size
                new_size = 0

    # single key 찾기
    def single_search(self, search_key):
        current = self
        # leaf노드 도달하면 여기서 value 구하기
        if current.isleaf:
            found = False
            print("leaf노드 도달")
            for i in current.nodelist:
                if i.key == search_key:
                    print("found : " + str(i.value))
                    found = True
                    break
            if not found:
                print("Not found")
            return
        # internal 노드면 해당 노드 리스트 키값 전부 출력
        else:
            for i in self.nodelist: # 출력
                print(i.key, end = ' ')
            print('')
            for i in range(len(current.nodelist)): # 이동
                # 왼쪽 자식으로 이동
                if search_key < current.nodelist[i].key:
                    current = current.nodelist[i].leftchild
                    break
                # 맨 마지막이면 오른쪽 자식으로 이동
                elif i == len(current.nodelist) - 1:
                    current = current.nodelist[i].rightchild
                else: # 다음 노드로 이동
                    continue
            # 자식 노드에서 다시 위치 찾기
            return current.single_search(search_key)
    
    # 범위 찾기
    def ranged_search(self, front, rear):
        current = self
        check = False
        # leaf노드 도달하면 여기서 범위 key, value 구하기
        if current.isleaf:
            print("leaf노드 도달")
            while current:
                for i in current.nodelist:
                    if i.key >= front and i.key <= rear:
                        print(i.key, i.value)
                    if i.key > rear:
                        check = True
                        break
                current = current.next
                if check:
                    break
            return
        else: # front 가 있을 리프 노드로 이동하기
            for i in range(len(current.nodelist)): # 이동
                # 왼쪽 자식으로 이동
                if front < current.nodelist[i].key:
                    current = current.nodelist[i].leftchild
                    break
                # 맨 마지막이면 오른쪽 자식으로 이동
                elif i == len(current.nodelist) - 1:
                    current = current.nodelist[i].rightchild
                # 다음 노드로 이동
                else:
                    continue
            # 자식 노드에서 다시 위치 찾기
            return current.ranged_search(front, rear)

    #부모 노드리스트에서 left, right 형제 찾기
    def find_l_r_i_nodelist(self, key):
        parent = self.parent
        for i in range(len(parent.nodelist)):
            if key < parent.nodelist[i].key:
                if i == 0:
                    return None, parent.nodelist[i].rightchild, i
                else:
                    return parent.nodelist[i-1].leftchild, parent.nodelist[i].rightchild, i
            if i == len(parent.nodelist) - 1:
                    return parent.nodelist[i].leftchild, None, i
    # # 삭제에서 필요한 합치기 함수
    # def merge(self, fnodelist, index):
    #     # 합치는건 무조건 부모의 값을 왼쪽에 삽입하고 오른쪽 nodelist를 붙인다
    #     lnodelist = fnodelist.parent.nodelist[index].leftchild
    #     rnodelist = fnodelist.parent.nodelist[index].rightchild
    #     parent = fnodelist.parent
    #     print("부모랑 밑에 왼 오 합칠거임 아래는 부모 키들")
    #     for i in parent.nodelist:
    #         print(i.key, end = ' ')
    #     print(' ')
    #     for i in lnodelist.nodelist:
    #         print(i.key, end = ' ')
    #     print(' ')
        
    #     # 합치다가 루트노드를 만났을 때(루트는 최소 키 개수 영향 x)
    #     if parent == self.head:
    #         print("부모가 루트일 때")
    #         node = parent.nodelist.pop(index)
    #         node.leftchild = lnodelist.nodelist[-1].rightchild
    #         node.rightchild = rnodelist.nodelist[0].leftchild
    #         # 왼쪽에 추가
    #         lnodelist.nodelist.append(node)
    #         for i in rnodelist.nodelist:
    #             lnodelist.nodelist.append(i)
    #         if len(parent.nodelist) > 0: # 루트에 다른 키가 남아있으면 자식 연결만 바꿔줌
    #             parent.nodelist[index].leftchild = lnodelist
    #         else: # 루트에 다른 키가 없으면 루트를 바꿔주고 리턴
    #             self.head = lnodelist
    #             return

    #     if lnodelist.isleaf:
    #         lnodelist.next = rnodelist.next
    #     # 일단 옮겨
    #     # -1 이거나 rnode랑 같으면 넣지 않고 합체
    #     if parent.nodelist[index].key == -1 or parent.nodelist[index].key == rnodelist.nodelist[0].key:
    #         print("-1 삭제 또는 같은 값 삭제")
    #         # 리프가 아니면 자식 재조정
    #         if not lnodelist.isleaf:
    #             lnodelist.nodelist[-1].rigthchild = rnodelist.nodelist[0].leftchild
    #         for i in rnodelist.nodelist:
    #             lnodelist.nodelist.append(i)
    #             print(str(i.key) + "를 옮김")
    #         # 선을 하나로 압축
    #         parent.nodelist[index].rightchild = lnodelist
    #         if parent.nodelist[index].key == -1:
    #             self.delete(parent, -1) # -1 삭제
    #         else:
    #             self.delete(parent, parent.nodelist[index].key) # 같은 값 삭제
    #     # 부모 노드에 있는 값 넣고 합체
    #     else:
    #         node = parent.nodelist[index]
    #         # 리프가 아니면 자식 재조정
    #         if not lnodelist.isleaf:
    #             if len(lnodelist.nodelist) > 0:
    #                 node.leftchild = lnodelist.nodelist[-1].rightchild
    #             if len(rnodelist.nodelist) > 0:
    #                 node.rightchild = rnodelist.nodelist[0].leftchild
    #         # 왼쪽에 추가
    #         lnodelist.nodelist.append(node)
    #         for i in rnodelist.nodelist:
    #             lnodelist.nodelist.append(i)
    #         parent.nodelist[index].leftchild = lnodelist
    #         if len(parent.nodelist) >= math.ceil(int(fnodelist.size)/2) - 1:
    #             return
    #         else:
    #             glnodelist, grnodelist, gk = parent.find_l_r_i_nodelist(node.key)
    #             # 맨 왼쪽이나 오른쪽 노드면 부모의 k인덱스의 왼쪽 오른쪽 합치기
    #             if (not glnodelist and grnodelist) or (glnodelist and not grnodelist):
    #                 self.merge(fnodelist, gk)
    #             # 나머지는 부모의 k-1인덱스의 왼쪽과 오른쪽 합치기(왼쪽 위주로 합치기)
    #             else:
    #                 self.merge(fnodelist, gk-1)
    # 삭제 함수
    def delete(self, fnodelist, key):
        index = 0
        # print(str(key)+"삭제")
        # 노드리스트에서 삭제할 노드의 인덱스 구하기
        for i in range(len(fnodelist.nodelist)):
            if fnodelist.nodelist[i].key == key:
                index = i
                break

        # 삭제해도 최소 키 수를 만족할 때
        if len(fnodelist.nodelist) > math.ceil(int(fnodelist.size)/2) - 1:
            # print("삭제해도 최소 키 수를 만족")
            # internal node이면 다음 노드랑 internal 노드랑 교체
            if fnodelist.nodelist[index].leftchild:
                pindex = fnodelist.nodelist[index].find_my_key_in_internal(key)
                internal_nodelist = fnodelist.nodelist[index].leftchild.parent
                internal_nodelist.nodelist[pindex] = fnodelist.nodelist[index+1]
                # 바꿔줄 때 child 조정
                if fnodelist.isleaf: # 리프 노드 일때
                    internal_nodelist.nodelist[pindex].leftchild = fnodelist.nodelist[index].leftchild
                    internal_nodelist.nodelist[pindex].rightchild = fnodelist.nodelist[index].rightchild
                else: # 부모 노드 일때
                    fnodelist.nodelist[index+1].leftchild = fnodelist.nodelist[index].leftchild
            fnodelist.nodelist.pop(index)         
        # 삭제하면 최소 키 수를 만족하지 못할 때
        else:
            # 형제에서 빌려온다
            # print("형제에서 빌려온다")
            lnodelist, rnodelist, k = fnodelist.find_l_r_i_nodelist(key)
            # 왼쪽 형제가 None이 아니고 빌려줄 수 있을 때
            if lnodelist and len(lnodelist.nodelist) > math.ceil(int(fnodelist.size)/2) - 1:
                if lnodelist.isleaf: # 리프 노드일때
                    # print("왼쪽에서 빌려온다")
                    node = lnodelist.nodelist.pop()
                    # print("빌릴 노드 키")
                    # print(node.key)
                    fnodelist.nodelist.pop(index)
                    fnodelist.nodelist.append(node)
                    fnodelist.nodelist.sort(key = lambda x : x.key)
                    # 부모 노드 리스트 재조정 및 자식 관리
                    node.leftchild = fnodelist.parent.nodelist[k].leftchild
                    node.rightchild = fnodelist.parent.nodelist[k].rightchild
                    fnodelist.parent.nodelist[k].leftchild = None
                    fnodelist.parent.nodelist[k].rightchild = None
                    fnodelist.parent.nodelist[k] = node
                else: # 부모 노드일 때
                    lnode = lnodelist.nodelist.pop()
                    pnode = fnodelist.parent.nodelist.pop()
                    tmp = lnode.rightchild
                    fnodelist.nodelist.append(pnode)
                    fnodelist.parent.nodelist.append(lnode)
                    lnode.leftchild = pnode.leftchild
                    lnode.rightchild = pnode.rigthchild
                    pnode.leftchild = tmp
                    pnode.rightchild = fnodelist.nodelist[0].leftchild
                    fnodelist.nodelist.sort(key = lambda x : x.key)
                    fnodelist.parent.nodelist.sort(key = lambda x : x.key)

            # 오른쪽 형제가 None이 아니고 빌려줄 수 있을 때
            elif rnodelist and len(rnodelist.nodelist) > math.ceil(int(fnodelist.size)/2) - 1:
                if rnodelist.isleaf: # 리프 노드일때 
                    # print("오른쪽에서 빌려온다")
                    # 오른쪽 형제에서 첫 번째 노드를 빌려옴
                    node = rnodelist.nodelist.pop(0)
                    # print("빌릴 노드 키: " + str(node.key))
                    fnodelist.nodelist.append(node)
                    # 오른쪽 형제의 첫 번째 노드의 자식 노드를 부모 노드와 연결
                    rnodelist.nodelist[0].leftchild = fnodelist.parent.nodelist[k].leftchild
                    rnodelist.nodelist[0].rightchild = fnodelist.parent.nodelist[k].rightchild
                    fnodelist.parent.nodelist[k] = rnodelist.nodelist[0]  # 부모 노드를 빌려온 노드로 교체
                    
                    # Internal 노드가 있을 경우 자식 노드의 참조를 수정
                    if fnodelist.nodelist[index].leftchild:
                        # print("Internal 노드가 있다면")
                        
                        # 부모에서 올바른 위치에 해당하는 노드를 찾음
                        pindex = fnodelist.nodelist[index].find_my_key_in_internal(key)
                        internal_nodelist = fnodelist.nodelist[index].leftchild.parent
                        
                        # 자식 노드 재배치 : 빌려온 노드를 부모에 추가
                        fnodelist.nodelist[index+1].leftchild = internal_nodelist.nodelist[pindex].leftchild
                        fnodelist.nodelist[index+1].rightchild = internal_nodelist.nodelist[pindex].rightchild
                        
                        # 부모 노드 갱신
                        internal_nodelist.nodelist[pindex] = fnodelist.nodelist[index+1]
                    # 삭제 후 노드 재배치
                    fnodelist.nodelist.pop(index)
                else: # 부모 노드일 때
                    rnode = rnodelist.nodelist.pop()
                    pnode = fnodelist.parent.nodelist.pop()
                    tmp = rnode.leftchild
                    fnodelist.nodelist.append(pnode)
                    fnodelist.parent.nodelist.append(rnode)
                    rnode.leftchild = pnode.leftchild
                    lnode.rightchild = pnode.rigthchild
                    pnode.rightchild = tmp
                    pnode.lefttchild = fnodelist.nodelist[-1].rightchild
                    fnodelist.parent.nodelist.sort(key = lambda x : x.key)
            # 형제한테 못빌리고 부모한테 도움을 받아야할 때
            # 이때 못하겠어서 리프노드에서 값만 삭제하도록 구현
            # 리프 노드가 최소 키 개수를 만족하지 못함
            else:
                # print("부모한테 도움 받기")
                fnodelist.nodelist.pop(index)

                # # 트리 구조 세팅을 먼저 하고 merge로 촥촥
                # print("부모한테 빌려온다 = 노드 합체")
                # # internal node에 대한 처리 먼저 해주기
                # if fnodelist.nodelist[index].leftchild:
                #     # internal nodelist 위치 찾기
                #     print("internal node 있음")
                #     pindex = fnodelist.nodelist[index].find_my_key_in_internal(key)
                #     internal_nodelist = fnodelist.nodelist[index].leftchild.parent
                #     # 다음 index가 있다면 거기서 갖고 온다
                #     # 다음 index는 internal node가 없어서 바로 처리해줄 수 있음
                #     if index + 1 < len(fnodelist.nodelist):
                #         fnodelist.nodelist[index+1].leftchild = fnodelist.nodelist[index].leftchild
                #         fnodelist.nodelist[index+1].rightchild = fnodelist.nodelist[index].rightchild
                #         fnodelist.nodelist[index].leftchild = None
                #         fnodelist.nodelist[index].rightchild = None
                #         internal_nodelist.nodelist[pindex] = fnodelist.nodelist[index+1]
                #     # 다음 index는 없고 rnodelist가 있으면 그 첫번째 값만 복사해옴
                #     elif rnodelist:
                #         print("rnode에서 갖고옴")
                #         internal_nodelist.nodelist[pindex].key = rnodelist.nodelist[0].key
                #         # internal_node에 다음거랑 같아질 수가 있음 이때 key를 -1로 설정한다
                #         if pindex + 1 < len(internal_nodelist.nodelist):
                #             if internal_nodelist.nodelist[pindex].key == internal_nodelist.nodelist[pindex+1].key:
                #                 print(internal_nodelist.nodelist[pindex].key)
                #                 print("근데 값이 같아서 이걸 -1로 바꿈")
                #                 internal_nodelist.nodelist[pindex].key = -1
                                
                #     # 다 없으면 그냥 없앰 key에 -1로 표현(트리 형태를 유지하기 위해)
                #     else:
                #         print("맨 오른쪽이라 -1 변경")
                #         internal_nodelist.nodelist[pindex].key = -1
                #         for i in internal_nodelist.nodelist:
                #             print(i.key)

                # # 리프노드에서 일단 제거 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # if fnodelist.isleaf:
                #     fnodelist.nodelist.pop(index) 
                #     print("리프 노드에서 일단 제거")
                    
                # # 맨 왼쪽이나 오른쪽 노드면 부모의 k인덱스의 왼쪽 오른쪽 합치기
                # if (not lnodelist and rnodelist) or (lnodelist and not rnodelist):
                #     print("맨 왼쪽이나 오른쪽 노드")
                #     self.merge(fnodelist, k)
                # # 나머지는 부모의 k-1인덱스의 왼쪽과 오른쪽 합치기(왼쪽 위주로 합치기)
                # else:
                #     print("중간")
                #     self.merge(fnodelist, k-1)
                
# pickle파일에서 bptree list 불러오기
def load_bptree_list():
    try:
        with open('bptree_list.pkl', 'rb') as file:
            # print("bplist 불러오기")
            return pickle.load(file)
    # 파일이 없으면 빈 리스트 반환
    except FileNotFoundError:
        # print("빈 bplsit 생성")
        return []

# pickle 파일에 bptree 추가하기(업데이트)
def update_bptree_list(bptree):
    bptree_list = load_bptree_list()
    # print("업데이트 전 : ", end = '')
    # print(bptree_list)
    updated = False
    # 기존 pickle 파일에 bptree 있으면 업데이트
    for i in range(len(bptree_list)):
        if bptree_list[i].file == bptree.file:
            bptree_list[i] = bptree
            updated = True
            # print("기존 bptree 덮음 : " + bptree.file)
            break
    # 기존 pickle에 없으면 bptree 추가
    if not updated:
        bptree_list.append(bptree)
        # print("bptree 새로 추가")
    # print("업데이트 후 : ", end = '')
    # print(bptree_list)
    # 업데이트 된 리스트를 다시 pickle 파일에 저장
    with open('bptree_list.pkl', 'wb') as file:
        pickle.dump(bptree_list, file)
    # print("bptree_list 업데이트")

# bptree 생성
def create_bptree(node_size, file):
    bptree = NodeList(node_size, file)
    bptree.head = bptree # 자기 자신을 가리킴
    # pickle 파일에 추가
    # print("pickle 파일에 추가")
    update_bptree_list(bptree)

#bptree 찾기
def load_bptree(bptree_list, file):
    # print("bptree 찾기")
    bptree = None
    for i in bptree_list:
        if i.file == file:
            # print("bptree 발견")
            bptree = i
            break
    return bptree

# data file 만들기
if sys.argv[1] == "-c":
    with open(sys.argv[2], 'w') as file:
        node_size = sys.argv[3]
        file.write("node_size : " + node_size)
        create_bptree(node_size, sys.argv[2])

# data file에 삽입하기
elif sys.argv[1] == "-i":
    node_list = []
    bptree_list = load_bptree_list()  # bptree_list 불러오기
    bptree = load_bptree(bptree_list, sys.argv[2])
    with open(sys.argv[2], 'r') as file:
        node_size = int(file.readline()[11:])

    with open(sys.argv[3], 'r') as file:
        reader = csv.reader(file)
        for row in file:
            key, value = map(int, row.strip().split(','))
            node = Node(key, value)
            node_list.append(node)
    # print("넣어야할 노드들 : ", end = '')
    # print(node_list)

    for node in node_list:
        fnodelist = bptree.head.find_position(node.key)
        # print("삽입시작" + str(node.key))
        bptree.insert(fnodelist, node)
    update_bptree_list(bptree)
    bptree.head.write_bptree_to_file(sys.argv[2])

# single key 찾기
elif sys.argv[1] == '-s':
    bptree_list = load_bptree_list()  # bptree_list 불러오기
    bptree = load_bptree(bptree_list, sys.argv[2])
    search_key = int(sys.argv[3])
    # print(str(search_key)+"찾기")
    bptree.head.single_search(search_key)

# 범위 찾기
elif sys.argv[1] == '-r':
    bptree_list = load_bptree_list()  # bptree_list 불러오기
    bptree = load_bptree(bptree_list, sys.argv[2])
    search_key_front = int(sys.argv[3])
    search_key_rear = int(sys.argv[4])
    # print(str(search_key_front) + "에서" + str(search_key_rear) + "까지 찾기")
    bptree.head.ranged_search(search_key_front, search_key_rear)

# data file에 삭제하기
elif sys.argv[1] == '-d':
    key_list = []
    bptree_list = load_bptree_list()  # bptree_list 불러오기
    bptree = load_bptree(bptree_list, sys.argv[2])
    with open(sys.argv[2], 'r') as file:
        node_size = int(file.readline()[11:])

    with open(sys.argv[3], 'r') as file:
        reader = csv.reader(file)
        for row in file:
            key = int(row)
            key_list.append(key)
    # print("삭제할 키들 : ", end = '')
    # print(key_list)

    for key in key_list:
        fnodelist = bptree.head.find_position(key)
        # print("삭제" + str(key))
        bptree.delete(fnodelist, key)
    update_bptree_list(bptree)
    bptree.head.write_bptree_to_file(sys.argv[2])