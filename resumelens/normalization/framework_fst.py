from resumelens.normalization.fst_builder import build_fst

FRAMEWORK_RULES = {
    "REACT": ["react.js", "reactjs", "react"],
    "ANGULAR": ["angular"],
    "VUE": ["vue.js", "vue"],
    "NODE_JS": ["node.js", "nodejs", "node"],
    "DJANGO": ["django"],
    "SPRING_BOOT": ["spring boot"],
    "PANDAS": ["pandas"],
    "NUMPY": ["numpy"],
    "SCIKIT_LEARN": ["scikit-learn", "scikit learn", "sklearn"],
    "TENSORFLOW": ["tensorflow", "tensor flow"],
    "PYTORCH": ["pytorch", "py torch"],
}

framework_fst = build_fst(FRAMEWORK_RULES)