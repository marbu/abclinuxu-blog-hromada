with System.Dim.Mks; use System.Dim.Mks;
procedure Example2 is
  len_a : Length := 10.0*m;
  len_b : Length := 15.0*m;
  surface : Area;
  len_sum : Length;
begin
  len_sum := len_a + len_b; -- ok
  surface := len_a * len_b; -- ok
  len_sum := len_a * len_b; -- invalid
end Example2;
