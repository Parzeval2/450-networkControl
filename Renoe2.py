import pandas as pd
def renoe(congestion_events):
    events = pd.read_csv(congestion_events)

    log = []

    CWD = 1
    SSTHRESH = 64

    for _, event in events.iterrows():
        if event['Congestion Event'] == 'Triple Duplicate':
            #if its a triple duplicate, we set the threshold  to half CWND, minimum 1
            SSTHRESH = max(CWD // 2, 1)
            CWD = SSTHRESH + 3
        elif event['Congestion Event'] == 'Retransmission':
            SSTHRESH = max(CWD // 2, 1)
            #if its a retransmission we go into slow start
            CWD = 1
        elif CWD < SSTHRESH:
            #exponential growth of congestion window
            CWD *= 2
        else:
            #if not in slow start, increase congestion window by 1
            CWD += 1

        log.append({
            'Timestamp': event['Timestamp'],
            'Event': event['Congestion Event'],
            'cwnd': CWD,
            'sstresh': SSTHRESH
        })

    pd.DataFrame(log).to_csv('reno.csv', index=False)
    print(f"Reno congestion control log saved to reno.csv")