import pandas as pd
def renoe(congestion_events):
    events = pd.read_csv(congestion_events)
    MSS = 1460
    log = []

    CWD = MSS
    SSTHRESH = 64 * MSS
    in_fast_recovery = False  # Track if Reno is in fast recovery

    for _, event in events.iterrows():
        if event['Congestion Event'] == 'Triple Duplicate':
            if not in_fast_recovery:
                SSTHRESH = max(CWD // 2, MSS)     # Enter Fast Recovery
                CWD = SSTHRESH + 3 * MSS
                in_fast_recovery = True
            else:
                # Increment CWD by 1 for each duplicate ACK in fast recovery
                CWD += MSS

        elif event['Congestion Event'] == 'Retransmission': 
            SSTHRESH = max(CWD // 2, MSS)     # Timeout: Exit fast recovery, set CWD to 1, re-enter slow start
            CWD = MSS
            in_fast_recovery = False
        else:
            if in_fast_recovery:
                CWD = SSTHRESH     # If a new ACK arrives, exit fast recovery, set CWD to SSTHRESH, and enter congestion avoidance
                in_fast_recovery = False
            else:
                if CWD < SSTHRESH:
                    CWD = min(2 * CWD, SSTHRESH)
                else:
                    CWD += MSS

        log.append({
            'Timestamp': event['Timestamp'],
            'Event': event['Congestion Event'],
            'cwnd': CWD,
            'sstresh': SSTHRESH,
            'Phase': 'Fast Recovery' if in_fast_recovery else ('Congestion Avoidance' if CWD >= SSTHRESH else 'Slow Start')
        })

    pd.DataFrame(log).to_csv('reno.csv', index=False)
    print("Reno congestion control log saved to reno.csv")
