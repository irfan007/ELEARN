from django import template
register=template.Library();
 
 
@register.filter
def getAndSet(req,arg):
    try:
            
        temp=req.session.get(str(arg),None)
        if temp:del req.session[str(arg)]
        return temp
    except:
        return None



# @register.filter
# def tf_toActualTerm(value):
#     terms=studentResult.all_terms
#     for t in terms:
#         if t[0]==value:
#             return t[1]
# 
# 
# @register.filter
# def tf_toActualStandard(value):
#     standards=studentResult.all_standards
#     for s in standards:
#         if s[0]==value:
#             return s[1]
# 
# 
# @register.filter
# def tf_toActualMedium(value):
#     mediums=studentInfo.all_mediums
#     for m in mediums:
#         if m[0]==value:
#             return m[1]