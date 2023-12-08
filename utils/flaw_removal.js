const CryptoJS = require("crypto").webcrypto;

var ze, ke = new Uint8Array(16)

function aa(e, a, t) {
    var l = (e = e || {}).random || (e.rng || qe)();
    if (l[6] = 15 & l[6] | 64,
    l[8] = 63 & l[8] | 128,
    a) {
        t = t || 0;
        for (var s = 0; s < 16; ++s)
            a[t + s] = l[s];
        return a
    }
    return ea(l)
}

function qe() {
    return CryptoJS.getRandomValues(ke)
}

const Je = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;
for (var Qe = [], Ge = 0; Ge < 256; ++Ge)
    Qe.push((Ge + 256).toString(16).substr(1));

function ea(e) {
    var a = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0
      , t = (Qe[e[a + 0]] + Qe[e[a + 1]] + Qe[e[a + 2]] + Qe[e[a + 3]] + "-" + Qe[e[a + 4]] + Qe[e[a + 5]] + "-" + Qe[e[a + 6]] + Qe[e[a + 7]] + "-" + Qe[e[a + 8]] + Qe[e[a + 9]] + "-" + Qe[e[a + 10]] + Qe[e[a + 11]] + Qe[e[a + 12]] + Qe[e[a + 13]] + Qe[e[a + 14]] + Qe[e[a + 15]]).toLowerCase();
    if (!function(e) {
        return "string" == typeof e && Je.test(e)
    }(t))
        throw TypeError("Stringified UUID is invalid");
    return t
}

console.log(aa())