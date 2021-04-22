
def aggregate_mturk_output(rows):
  final = []

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

    pair1 = (profile, p1)
    pair2 = (profile, p2)
    pair3 = (profile, p3)
    pair4 = (profile, p4)
    pair5 = (profile, p5)
    
    final.append((wrkr, pair1, r1))
    final.append((wrkr, pair2, r2))
    final.append((wrkr, pair3, r3))
    final.append((wrkr, pair4, r4))
    final.append((wrkr, pair5, r5))

  final.sort()
  return final