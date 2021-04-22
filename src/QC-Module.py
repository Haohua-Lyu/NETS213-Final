def em_worker_quality(rows, labels):
  worker = {}
  t_match = 0
  t_nmatch = 0
  for l in labels.items():
    if l[1]["match"] == 1.0:
      t_match += 1
    elif l[1]["notmatch"] == 1.0:
      t_nmatch += 1
  
  for _, r in rows.iterrows():
    wrkr = r['WorkerId']
    profile = r['Input.given_profile']
    p1 = r['Input.profile1']
    p2 = r['Input.profile2']
    p3 = r['Input.profile3']
    p4 = r['Input.profile4']
    p5 = r['Input.profile5']
    r1 = r['Answer.rating1']
    r2 = r['Answer.rating2']
    r3 = r['Answer.rating3']
    r4 = r['Answer.rating4']
    r5 = r['Answer.rating5']

    if worker.get(wrkr) == None:
      worker.update({wrkr: {"match_match": 0.0, "match_notmatch": 0.0, 
                            "notmatch_notmatch": 0.0, "notmatch_match": 0.0}})
    # rating of 3 and 4 means a match
    if r1 in ['3', '4']:
      if labels[(profile, p1)]["match"] == 1.0:
        worker[wrkr]["match_match"] += 1.0
      elif labels[(profile, p1)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_match"] += 1.0
    # rating of 1 and 2 means a NO match
    elif r1 in ['1', '2']:
      if labels[(profile, p1)]["match"] == 1.0:
        worker[wrkr]["match_notmatch"] += 1.0
      elif labels[(profile, p1)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_notmatch"] += 1.0
    
    # rating of 3 and 4 means a match
    if r2 in ['3', '4']:
      if labels[(profile, p2)]["match"] == 1.0:
        worker[wrkr]["match_match"] += 1.0
      elif labels[(profile, p2)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_match"] += 1.0
    # rating of 1 and 2 means a NO match
    elif r2 in ['1', '2']:
      if labels[(profile, p2)]["match"] == 1.0:
        worker[wrkr]["match_notmatch"] += 1.0
      elif labels[(profile, p2)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_notmatch"] += 1.0
    
    # rating of 3 and 4 means a match
    if r3 in ['3', '4']:
      if labels[(profile, p3)]["match"] == 1.0:
        worker[wrkr]["match_match"] += 1.0
      elif labels[(profile, p3)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_match"] += 1.0
    # rating of 1 and 2 means a NO match
    elif r3 in ['1', '2']:
      if labels[(profile, p3)]["match"] == 1.0:
        worker[wrkr]["match_notmatch"] += 1.0
      elif labels[(profile, p3)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_notmatch"] += 1.0
    
    # rating of 3 and 4 means a match
    if r4 in ['3', '4']:
      if labels[(profile, p4)]["match"] == 1.0:
        worker[wrkr]["match_match"] += 1.0
      elif labels[(profile, p4)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_match"] += 1.0
    # rating of 1 and 2 means a NO match
    elif r4 in ['1', '2']:
      if labels[(profile, p4)]["match"] == 1.0:
        worker[wrkr]["match_notmatch"] += 1.0
      elif labels[(profile, p4)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_notmatch"] += 1.0
    
    # rating of 3 and 4 means a match
    if r5 in ['3', '4']:
      if labels[(profile, p5)]["match"] == 1.0:
        worker[wrkr]["match_match"] += 1.0
      elif labels[(profile, p5)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_match"] += 1.0
    # rating of 1 and 2 means a NO match
    elif r5 in ['1', '2']:
      if labels[(profile, p5)]["match"] == 1.0:
        worker[wrkr]["match_notmatch"] += 1.0
      elif labels[(profile, p5)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_notmatch"] += 1.0
  
  for worker, matrix in worker.items():
    if t_match != 0.0:
      matrix["match_match"] = matrix["match_match"] / t_match
      matrix["match_notmatch"] = matrix["match_notmatch"] / t_match
    if t_nmatch != 0.0:
      matrix["notmatch_notmatch"] = matrix["notmatch_notmatch"] / t_nmatch
      matrix["notmatch_match"] = matrix["notmatch_match"] / t_nmatch
  return worker

def em_votes(rows, worker_qual):
    labels = {}
    for _, r in rows.iterrows():
      wrkr = r['WorkerId']
      profile = r['Input.given_profile']
      p1 = r['Input.profile1']
      p2 = r['Input.profile2']
      p3 = r['Input.profile3']
      p4 = r['Input.profile4']
      p5 = r['Input.profile5']
      r1 = r['Answer.rating1']
      r2 = r['Answer.rating2']
      r3 = r['Answer.rating3']
      r4 = r['Answer.rating4']
      r5 = r['Answer.rating5']

      if labels.get((profile, p1)) == None:
        labels.update({(profile, p1): {"match": 0.0, "notmatch": 0.0}})
      if labels.get((profile, p2)) == None:
        labels.update({(profile, p2): {"match": 0.0, "notmatch": 0.0}})
      if labels.get((profile, p3)) == None:
        labels.update({(profile, p3): {"match": 0.0, "notmatch": 0.0}})
      if labels.get((profile, p4)) == None:
        labels.update({(profile, p4): {"match": 0.0, "notmatch": 0.0}})
      if labels.get((profile, p5)) == None:
        labels.update({(profile, p5): {"match": 0.0, "notmatch": 0.0}})
    
      if r1 in ['3', '4']:
          labels[(profile, p1)]["match"]+= worker_qual[wrkr]["match_match"] * int(r1)
          labels[(profile, p1)]["notmatch"] += worker_qual[wrkr]["notmatch_match"] * int(r1)
      elif r1 in ['1', '2']:
          labels[(profile, p1)]["notmatch"] += worker_qual[wrkr]["notmatch_notmatch"] * int(r1)
          labels[(profile, p1)]["match"] += worker_qual[wrkr]["match_notmatch"] * int(r1)
      if r2 in ['3', '4']:
          labels[(profile, p2)]["match"]+= worker_qual[wrkr]["match_match"] * int(r2)
          labels[(profile, p2)]["notmatch"] += worker_qual[wrkr]["notmatch_match"] * int(r2)
      elif r2 in ['1', '2']:
          labels[(profile, p2)]["notmatch"] += worker_qual[wrkr]["notmatch_notmatch"] * int(r2)
          labels[(profile, p2)]["match"] += worker_qual[wrkr]["match_notmatch"] * int(r2)
      if r3 in ['3', '4']:
          labels[(profile, p3)]["match"]+= worker_qual[wrkr]["match_match"] * int(r3)
          labels[(profile, p3)]["notmatch"] += worker_qual[wrkr]["notmatch_match"] * int(r3)
      elif r3 in ['1', '2']:
          labels[(profile, p3)]["notmatch"] += worker_qual[wrkr]["notmatch_notmatch"] * int(r3)
          labels[(profile, p3)]["match"] += worker_qual[wrkr]["match_notmatch"] * int(r3)
      if r4 in ['3', '4']:
          labels[(profile, p4)]["match"]+= worker_qual[wrkr]["match_match"] * int(r4)
          labels[(profile, p4)]["notmatch"] += worker_qual[wrkr]["notmatch_match"] * int(r4)
      elif r4 in ['1', '2']:
          labels[(profile, p4)]["notmatch"] += worker_qual[wrkr]["notmatch_notmatch"] * int(r4)
          labels[(profile, p4)]["match"] += worker_qual[wrkr]["match_notmatch"] * int(r4)
      if r5 in ['3', '4']:
          labels[(profile, p5)]["match"]+= worker_qual[wrkr]["match_match"] * int(r5)
          labels[(profile, p5)]["notmatch"] += worker_qual[wrkr]["notmatch_match"] * int(r5)
      elif r5 in ['1', '2']:
          labels[(profile, p5)]["notmatch"] += worker_qual[wrkr]["notmatch_notmatch"] * int(r5)
          labels[(profile, p5)]["match"] += worker_qual[wrkr]["match_notmatch"] * int(r5)
    
    maj_labels = {}
    for pair, val in labels.items():
      if val["notmatch"] > val["match"]:
        maj_labels.update({pair: {"match": 0.0, "notmatch": 1.0}})
      else:
        maj_labels.update({pair: {"match": 1.0, "notmatch": 0.0}})
    
    return maj_labels
    

def em_iteration(rows, worker_qual):
    labels = em_votes(rows, worker_qual)
    worker_qual = em_worker_quality(rows, labels)
    return labels, worker_qual

def em_vote(rows, iter_num):
  worker_qual = {}
  for _, row in rows.iterrows():
    wrkr = row['WorkerId']
    if worker_qual.get(wrkr) == None:
      worker_qual.update({wrkr: {"match_match": 1.0, "match_notmatch": 0.0, 
                                    "notmatch_notmatch": 1.0, "notmatch_match": 0.0}})
  
  wrkr_ql = worker_qual
  labels = ""
  for i in range(iter_num):
      (l, w_ql) = em_iteration(rows, wrkr_ql) 
      wrkr_ql = w_ql
      labels = l

  final = []
  for pair, val in labels.items():
    if val["match"] == 1.0:
      final.append((pair, "match"))
    else:
      final.append((pair, "notmatch"))

  final.sort()
  return final