[<Measure>] type m

let len_a = 10.0<m>
let len_b = 15.0<m>
let len_sum : float<m>   = len_a + len_b // ok
let surface : float<m^2> = len_a * len_b // ok
let len_c   : float<m>   = len_a * len_b // invalid
