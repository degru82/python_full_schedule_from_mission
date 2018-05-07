import MySQLdb
import logging
logger = logging.getLogger('mssn-db')

class db_if:
    def __init__(self):
        self._db = MySQLdb.connect(host='localhost', user='root', db='AVFMS')
        logger.debug(f'DB: {self._db}')
        
        self._cursor = self._db.cursor()

    def query(self, qrystr):
        self._cursor.execute(qrystr)
        return self._cursor.fetchall()
    
    def manipulate(self, qrystr):
        self._cursor.execute(qrystr)
        self._db.commit()

avfmsdb = db_if()







def get_stoppoints():
    qry = f'''
        select STOPPOINT_ID, ROUT_LINK_ID, JRNY_PATTRN_ID
        from tb_stoppoint
    '''
    result = avfmsdb.query(qry)

    stoppoints = []
    for row in result:
        stop = {}
        stop['stoppointId'] = row[0]
        stop['routLinkId'] = row[1]
        stop['jrnyPattrnId'] = row[2]
        stoppoints.append(stop)

    return stoppoints


def service_requested_as(servreq):
    qry = f'''
        select SVC_REQ_ID from tb_servicerequest
    '''
    result = avfmsdb.query(qry)
    if len(result) == 0:
        svcreqid = 'SR_1000001'
    else:
        org = result[-1][0]
        org_max_num = int(org[3:])
        svcreqid = 'SR_' + str(org_max_num + 1).zfill(7)

    qry = f'''
        insert into tb_servicerequest
        (SVC_REQ_ID, PICKUP_STOPPOINT_ID, DROPOFF_STOPPOINT_ID, NUM_OF_PASSNGR)
        values
        ("{svcreqid}", "{servreq["from"]}", "{servreq["to"]}", {servreq["numofpassngr"]})
    '''
    avfmsdb.manipulate(qry)

    full_schedule = get_full_schedule()
    logger.debug(f'FULL SCHEDULE GENERATED:\n{full_schedule}')

    return svcreqid, full_schedule

def update_schedule(svcreqid, svc_req):
    # check if there's existing stop schedule for pickup stop
    pickupstop = svc_req['from']
    numofpassngr = svc_req['numofpassngr']
    mssn_id = find_or_create_mssion_for(pickupstop, numofpassngr)
    


def find_or_create_mssion_for(pickupstop, num_geton):
    mssn_id = None

    round_schedule = get_full_schedule()
    for sched in round_schedule:
        msn = sched['mssnId']
        stopid = sched['stoppointId']
        accumnum = sched['passngrChange']
        visitseq = sched['visitSeq']
        if stopid == pickupstop and accumnum + num_geton < 5:
            if msn == None:
                create_mission(stopid, visitseq, accumnum)
            else:
                update_mission(msn, accumnum + num_geton)
            break
    
    return mssn_id


def create_mission(stop_id, visit_seq, accum_num_passngr):
    pass

def update_mission(stop_id, accum_num_passngr):
    pass



def get_servreq():
    qry = f'''
        select 
            SVC_REQ_ID,
            PICKUP_STOPPOINT_ID,
            MSSN_ID_FOR_PICKUP,
            DROPOFF_STOPPOINT_ID,
            MSSN_ID_FOR_DROPOFF,
            NUM_OF_PASSNGR
        from
            tb_servicerequest
    '''
    result = avfmsdb.query(qry)
    requests = []
    for row in result:
        req = {}
        req['svcReqId'] = row[0]
        req['pickupStoppointId'] = row[1]
        req['mssnIdForPickup'] = row[2]
        req['dropoffStoppointId'] = row[3]
        req['mssnIdForDropoff'] = row[4]
        req['numOfPassngr'] = row[5]
        requests.append(req)
    
    return requests


def get_single_round():
    qry = f'''
        SELECT
            LoR.ROUT_LINK_ID,
            STP.STOPPOINT_ID

        FROM
            tb_linkonroute LoR
        JOIN tb_stoppoint STP
        ON LoR.ROUT_LINK_ID = STP.ROUT_LINK_ID

        ORDER BY
            LoR.LINK_SEQ ASC
    '''
    result = avfmsdb.query(qry)
    single_round_schedule = []
    for idx, row in enumerate(result):
        sched = {}
        sched['routLinkId'] = row[0]
        sched['stoppointId'] = row[1]
        sched['visitSeq'] = idx + 1
        sched['mssnId'] = None
        sched['passngrChange'] = 0
        single_round_schedule.append(sched)
    
    logger.debug(f'ROUND SCHEDULE CONSTRUCTED AS:\n{single_round_schedule}')
    return single_round_schedule
    

def get_full_schedule():
    roundschedule = get_single_round()

    qry = f'''
        SELECT
            MSSN_ID,
            VISIT_SEQ,
            PASSNGR_CHANGE
        FROM
            tb_mission
        ORDER BY
            VISIT_SEQ ASC
    '''
    result = avfmsdb.query(qry)
    missions = []
    for row in result:
        msn = {}
        msn['mssnId'] = row[0]
        msn['visitSeq'] = int(row[1])
        msn['passngrChange'] = int(row[2])
        missions.append(msn)

    # extends roundschedule by visitSeq in mission
    maxindex = missions[-1]['visitSeq']
    logger.debug(f'MAX SEQ NUMBER OF VISIT:\n\t{maxindex}')
    while len(roundschedule) < maxindex:
        extend_round(roundschedule)
    # extends one more round to make it easy to add the new round
    logger.debug(f'SCHEDULE W/ EXTENDED ROUNDS LENGTH:\n\t{len(roundschedule)}')
    logger.debug(f'SCHEDULE W/ EXTENDED ROUNDS CONTENTS:\n\t{roundschedule}')
    extend_round(roundschedule)
    logger.debug(f'SCHEDULE W/ EXTENDED ROUNDS:\n\t{roundschedule}')
    
    psngr_cabin = 0
    for sched in roundschedule:
        sched['accumNumPassngr'] = psngr_cabin
        
        seq = sched['visitSeq']
        cur_mssn = {}
        for mssn in missions:
            if mssn['visitSeq'] == seq:
                cur_mssn = mssn
        
        if bool(cur_mssn):
            logger.debug(f'CURRENT MISSION TO ADD SCHEDULE\n{cur_mssn}')
            sched['accumNumPassngr'] += cur_mssn['passngrChange'] 
            sched['mssnId'] = cur_mssn['mssnId']
            sched['passngrChange'] = cur_mssn['passngrChange']

        psngr_cabin = sched['accumNumPassngr']
        
    return roundschedule
    
def extend_round(roundschedule):
    new_round = get_single_round()
    last_offset = roundschedule[-1]['visitSeq']
    for sched in new_round:
        sched['visitSeq'] += (last_offset)
        sched['mssnId'] = None
        sched['passngrChange'] = 0
        roundschedule.append(sched)

    logger.debug(f'ROUND SCHEUDLE EXTENDED AS:\n{roundschedule}')
    return roundschedule

    