from resumelens.normalization.tech_fst import language_fst, database_fst, tool_fst
from resumelens.normalization.framework_fst import framework_fst   # Devia (D4)

# union = un solo transductor que acepta lo que acepte cualquiera de los 4
ALL_FST = (framework_fst.union(language_fst)
                        .union(database_fst)
                        .union(tool_fst))

def normalize_token(token):
    outputs = list(ALL_FST.translate(list(token.lower())))
    if outputs:
        return outputs[0][0]
    return None

def normalize_all(extracted):
    result = []
    for category in ["languages", "frameworks", "databases", "tools"]:
        for token in extracted.get(category, []):
            canonical = normalize_token(token)
            if canonical is not None and canonical not in result:
                result.append(canonical)
    return result