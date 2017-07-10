# recent pass test


import json
import os

from collections import OrderedDict

# self made function library
from NetworkGraph import purchase, befriend, unfriend, getNetworkNode, checkAnomaly


""
##############################################################
# Read the file and create the following
# (1)create network state with purchase history for node and
# (2) total purchase History
##############################################################
""
graphState = dict()
pN = 0
purchaseHistory = dict({'pN':pN})
lineN = 1
with open(os.path.join(os.path.dirname(__file__), '..', 'log_input/batch_log.json')) as f:
# with open(os.path.join(os.path.dirname(__file__), '..', 'sample_dataset/batch_log.json')) as f:

    dictSel = json.loads(f.readline())

    D = int(dictSel.get(u'D', '1'))  # also has fall back default values
    T = int(dictSel.get(u'T', '5'))  # also has fall back default values

    for line in f:
        print('Processing Line {} of batch file'.format(lineN))
        lineN += 1
        dictSel = json.loads(line)
        event_type = dictSel.get(u'event_type', 'empty')

        # FRIENDING ACTION
        if event_type == u'befriend':
            befriend(graphState, dictSel)
            # print('Friending')


        # UNFRIENDING ACTION
        elif (event_type == u'unfriend'):
            unfriend(graphState, dictSel)


        # PURCHASING ACTION (need only upto T purchases for each customer)
        elif event_type == u'purchase':
            purchase(graphState, dictSel, purchaseHistory, T)
            # pN += 1


# del dictSel, f, line
del dictSel, f, line, event_type




""
###############################################################################
# Go through an activity at a time in stream ######
# if befriend --> update edge, flag need to recompute mean, sd
# if unfriend --> update edge, flag need to recompute mean, sd
# if purchase by a customer
#   -> (1) see if its considered anomalous by any network node -> flag, continue
#          (1a) for a node, get its network nodes of degree 'D'
#   -> (2) update purchaseHistory, graphState
###############################################################################
""
open(os.path.join(os.path.dirname(__file__),'..','log_output/flagged_purchases.json'), 'a').close()
startDumping = 1
with open(os.path.join(os.path.dirname(__file__),'..','log_input/stream_log.json')) as f:
# with open(os.path.join(os.path.dirname(__file__), '..', 'sample_dataset/stream_log.json')) as f:
    lineN = 1
    for line in f:
        print('Processing Line {} of stream file'.format(lineN))
        lineN +=1
        dictSel = json.loads(line,  object_pairs_hook=OrderedDict)
        # print(dictSel)

        event_type = dictSel.get(u'event_type', 'empty')

        # FRIENDING ACTION
        if event_type == u'befriend':
            befriend(graphState, dictSel)
            graphState['last_Friending_Unfriending'] = dictSel


        # UNFRIENDING ACTION
        elif (event_type == u'unfriend'):
            unfriend(graphState, dictSel)
            graphState['last_Friending_Unfriending'] = dictSel

        # PURCHASING ACTION (need only upto T purchases for each customer)
        elif event_type == u'purchase':
            anomalous = checkAnomaly(dictSel.get(u'id'), graphState, dictSel, D, T, purchaseHistory)

            if anomalous[0]:
                with open(os.path.join(os.path.dirname(__file__), '..', 'log_output/flagged_purchases.json'),
                          "a") as outputFile:
                    dictSel.update({'sd': '%.2f' % (anomalous[1][1]), 'mean': '%.2f' % (anomalous[1][0])})
                    if not (startDumping):
                        outputFile.write('\n')
                    json.dump(dictSel, outputFile)
                    startDumping = 0
                    # print('Flagged')

            purchase(graphState,dictSel, purchaseHistory,T)
