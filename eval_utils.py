class DSTEvaluator:
    def __init__(self, slot_meta):
        self.slot_meta = slot_meta
        self.joint_goal_hit = 0
        self.all_hit = 0
        self.slot_turn_acc = 0
        self.slot_f1_pred = 0
        self.slot_f1_count = 0

    def update(self, gold, pred):
        self.all_hit += 1
        if set(pred) == set(gold):
            self.joint_goal_hit += 1
        temp_acc = compute_acc(gold, pred, self.slot_meta)
        self.slot_turn_acc += temp_acc
        temp_f1, _, _, count = compute_prf(gold, pred)
        self.slot_f1_pred += temp_f1
        self.slot_f1_count += count

    def compute(self):
        turn_acc_score = self.slot_turn_acc / self.all_hit
        slot_f1_score = self.slot_f1_pred / self.slot_f1_count
        joint_goal_accuracy = self.joint_goal_hit / self.all_hit
        eval_result = {
            "joint_goal_accuracy": joint_goal_accuracy,
            "turn_slot_accuracy": turn_acc_score,
            "turn_slot_f1": slot_f1_score,
        }
        return eval_result


def compute_acc(gold, pred, slot_meta):
    miss_gold = 0
    miss_slot = []
    for g in gold:
        if g not in pred:
            miss_gold += 1
            miss_slot.append(g.rsplit("-", 1)[0])
    wrong_pred = 0
    for p in pred:
        if p not in gold and p.rsplit("-", 1)[0] not in miss_slot:
            wrong_pred += 1
    acc_total = len(slot_meta)
    acc = len(slot_meta) - miss_gold - wrong_pred
    acc /= float(acc_total)
    return acc


def compute_prf(gold, pred):
    TP, FP, FN = 0, 0, 0
    if len(gold) != 0:
        count = 1
        for g in gold:
            if g in pred:
                TP += 1
            else:
                FN += 1
        for p in pred:
            if p not in gold:
                FP += 1
        precision = TP / float(TP + FP) if (TP + FP) != 0 else 0
        recall = TP / float(TP + FN) if (TP + FN) != 0 else 0
        f1 = (
            2 * precision * recall / float(precision + recall)
            if (precision + recall) != 0
            else 0
        )
    else:
        if len(pred) == 0:
            precision, recall, f1, count = 1, 1, 1, 1
        else:
            precision, recall, f1, count = 0, 0, 0, 1
    return f1, recall, precision, count
