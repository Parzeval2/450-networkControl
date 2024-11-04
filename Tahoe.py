import pandas as pd
def tahoe(congestion_events):
    events = pd.read_csv(congestion_events)
    MSS = 1460
    CWND = MSS #we set the congestiong window to an arbitrary 1
    SSTHRESH = 64 * MSS #we set the slow start thresh to an arbitrary "large number" 64

    log = []

    for _, event in events.iterrows():
        if event['Congestion Event'] == 'Triple Duplicate' or event['Congestion Event'] == 'Retransmission':
            #if there is a congestion event, we update the slow start threshold to half of the current CWND, but not less than 1
            #we then set the congestion window to 1 sto begin the slow start phase
            SSTHRESH = max(CWND // 2, MSS)
            CWND = MSS
        elif CWND < SSTHRESH:
            #slow start phase, exponential growth
            CWND = min(2 * CWND, SSTHRESH)
        else:
            #linear growth
            CWND += MSS
        log.append({
            'Timestamp': event['Timestamp'],
            'Congestion Event': event['Congestion Event'],
            'cwnd': CWND,
            'sshthresh': SSTHRESH
        })

    pd.DataFrame(log).to_csv('tahoe_cwnd.csv', index=False)
    print("Tahoe congestion control log saved to tahoe_cwnd.csv")