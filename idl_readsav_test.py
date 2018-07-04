from scipy.io.idl import readsav
f = readsav('d:/bogomaz/download/t_GUVI_im_limb_v013r00_2007215_REV30603.L2B.sav')
for k in f:
    print(k)
with open('d:/test.txt', 'w') as file:
    file.write(str(f))