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
    profile1 = r['Profile1']
    profile2 = r['Profile2']
    rating = r['Rating']

    if worker.get(wrkr) == None:
      worker.update({wrkr: {"match_match": 0.0, "match_notmatch": 0.0, 
                            "notmatch_notmatch": 0.0, "notmatch_match": 0.0}})
    # rating of 3 and 4 means a match
    if rating in ['3', '4']:
      if labels[(profile1, profile2)]["match"] == 1.0:
        worker[wrkr]["match_match"] += 1.0
      elif labels[(profile1, profile2)]["notmatch"] == 1.0:
        worker[wrkr]["notmatch_match"] += 1.0
    # rating of 1 and 2 means a NO match
    elif rating in ['1', '2']:
      if labels[(profile1, profile2)]["match"] == 1.0:
        worker[wrkr]["match_notmatch"] += 1.0
      elif labels[(profile1, profile2)]["notmatch"] == 1.0:
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
      profile1 = r['Profile1']
      profile2 = r['Profile2']
      rating = r['Rating']

      if labels.get((profile1, profile2)) == None:
        labels.update({(profile1, profile2): {"match": 0.0, "notmatch": 0.0}})

      if rating in ['3', '4']:
          labels[(profile1, profile2)]["match"]+= worker_qual[wrkr]["match_match"] * int(r1)
          labels[(profile1, profile2)]["notmatch"] += worker_qual[wrkr]["notmatch_match"] * int(r1)
      elif rating in ['1', '2']:
          labels[(profile1, profile2)]["notmatch"] += worker_qual[wrkr]["notmatch_notmatch"] * int(r1)
          labels[(profile1, profile2)]["match"] += worker_qual[wrkr]["match_notmatch"] * int(r1)
      
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