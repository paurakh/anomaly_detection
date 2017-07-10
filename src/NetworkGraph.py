import math
import time
import datetime



#######################################################################################
def purchase(graphState, dictSel, purchaseHistory, T):

    #  make unique key
    unixTS = time.mktime(datetime.datetime.strptime(dictSel[u'timestamp'], "%Y-%m-%d %H:%M:%S").timetuple())
    uniqueID = 1

    if unixTS in purchaseHistory:

        unixTS_unique = unixTS + purchaseHistory[unixTS][1] * 1e-6
        uniqueID = purchaseHistory[unixTS][1]+1
        purchaseHistory[unixTS][1] = uniqueID
    else:
        unixTS_unique = unixTS
    # while unixTS in purchaseHistory:
    #     unixTS += 1e-6

    pN = unixTS_unique

    # put it in the graph
    # if already exists
    if dictSel.get(u'id') in graphState:
        graphState[dictSel.get(u'id')]['purchase'].append(pN)  # can simply append coz already exist
        # if list already contains T purchases,
        # (1) remove the u'id' 's first one from purchase history
        # (2) loose the first earliests
        if len(graphState[dictSel.get(u'id')]['purchase']) > T:
            # del purchaseHistory[graphState[dictSel.get(u'id')]['purchase'][0]]
            purchaseHistory.pop(graphState[dictSel.get(u'id')]['purchase'][0], None)
            graphState[dictSel.get(u'id')]['purchase'].pop(0)
    # if does not exist
    else:
        graphState[dictSel.get(u'id')] = {'neighbors': set(),
                                          'purchase': [pN]}  # need to create new key
                                          # 'network_T_purchase': [],
                                          # 'last_Friending_Unfriending': {}}  # need to create new key coz never seen b4
    purchaseHistory.update({pN: [dictSel, uniqueID]})
    # pN += 1
    purchaseHistory.update({'pN': pN})

#######################################################################################
def befriend(graphState, dictSel):
    if dictSel.get(u'id1') in graphState:
        graphState[dictSel.get(u'id1')]['neighbors'].update({dictSel.get(u'id2', 'empty')})  # can simply append
    else:
        graphState[dictSel.get(u'id1')] = {'neighbors': {dictSel.get(u'id2', 'empty')},
                                           'purchase': []}
                                           # 'network_T_purchase': [],
                                           # 'last_Friending_Unfriending': {}}  # need to create new key

    if dictSel.get(u'id2') in graphState:
        graphState[dictSel.get(u'id2')]['neighbors'].update({dictSel.get(u'id1', 'empty')})  # can simply append
    else:
        graphState[dictSel.get(u'id2')] = {'neighbors': {dictSel.get(u'id1', 'empty')},
                                           'purchase': []}  # need to create new key
                                           # 'network_T_purchase': [],
                                           # 'last_Friending_Unfriending': {}}

#######################################################################################
def unfriend(graphState, dictSel):
    # print('Unfriending')
    if dictSel.get(u'id1') in graphState:
        graphState[dictSel.get(u'id1')]['neighbors'].remove(dictSel.get(u'id2', 'empty'))
    if dictSel.get(u'id2') in graphState:
        graphState[dictSel.get(u'id2')]['neighbors'].remove(dictSel.get(u'id1', 'empty'))

#######################################################################################
def getNetworkNode(node, nodeParent, graphState, DEff,networkNodeSet):
    networkNodeSet.update(graphState[node]['neighbors'] - {nodeParent}) # set data type to remove the repetition, remember to remove self
    # make this a recursive function
    # base case
    if DEff == 0 :
        return networkNodeSet

    # resursive case
    for nextNode in graphState[node]['neighbors']:
        if (nextNode == nodeParent):
            # prevent chain recursion with parent node
            return networkNodeSet
        getNetworkNode(nextNode, nodeParent, graphState, DEff-1, networkNodeSet)
    return networkNodeSet

#######################################################################################
def getMeanStd(networkNode, T, graphState, purchaseHistory, selNetworkNode):

    if 0: #bool(graphState[selNetworkNode]['network_T_purchase']) & (graphState['last_Friending_Unfriending'] == graphState[selNetworkNode]['last_Friending_Unfriending']):
        indPurchase = graphState[selNetworkNode]['network_T_purchase']
    else:
        T_purchase =[]
        nP = 0
        for node in networkNode:
            # print graphState[node]['purchase']
            if list(graphState[node]['purchase']):
                T_purchase.append(list(graphState[node]['purchase']))
                nP += len(graphState[node]['purchase'])

        # nP -= len(T_purchase)
        # if nP < 2: return [float('inf'), float('inf')]
        #    take the greatest T numbers from the sorted nested list (can exploit by starting from the end)
        indPurchase = []
        for i in range(T-1):
            indC = [x[-1] for x in T_purchase]
            indMax, indPop = max((indC[j], j) for j in xrange(len(indC)))
            indPurchase.append(indMax)
            T_purchase[indPop].pop()
            if not T_purchase[indPop]:
                del T_purchase[indPop]
            if not T_purchase: break

    # graphState[selNetworkNode]['last_Friending_Unfriending'] = graphState['last_Friending_Unfriending']


    # indPurchase = [17, 16, 15, 14, 13]
    if len(indPurchase) < 2:
        # graphState[selNetworkNode]['network_T_purchase'] = indPurchase
        return [float('inf'), float('inf')]

    amountVal = [float(purchaseHistory[x][0]['amount']) for x in indPurchase]
    # amountVal = [10, 20, 30, 40, 50]

    # graphState[selNetworkNode]['network_T_purchase'] = indPurchase
    meanVal = sum(amountVal)/len(amountVal)
    stdVal = math.sqrt(sum([(meanVal-d)*(meanVal-d) for d in amountVal]) / len(amountVal))
    # return meanVal ,stdVal
    return [meanVal, stdVal]


########################################################################################
def checkAnomaly(selNetworkNode, graphState, dictSel, D, T, purchaseHistory):
    # find all the network nodes
    # Arrange last T purchases in chronological order
    # select the last T purchases
    # compute the mean and the standard deviation
    # return 0 or 1

    networkNode = getNetworkNode(selNetworkNode, selNetworkNode, graphState, D,
                                 set())  # these are the network nodeeee
    statsPurchases = getMeanStd(networkNode, T, graphState, purchaseHistory, selNetworkNode)
    return [float(dictSel[u'amount']) > statsPurchases[0] + 3 * statsPurchases[1], statsPurchases]
