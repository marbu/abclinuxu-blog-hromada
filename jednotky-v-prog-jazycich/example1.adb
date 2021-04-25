procedure Example1 is
  type Meters is new Float;
  type Meters_Squared is new Float;
  function "*" (Left, Right : Meters) return Meters_Squared is
  begin
    return Meters_Squared(Float(Left)*Float(Right));
  end;
  function "*" (Left, Right : Meters) return Meters is abstract;
  len_a : Meters := 10.0;
  len_b : Meters := 15.0;
  surface : Meters_Squared;
  len_sum : Meters;
begin
  len_sum := len_a + len_b; -- ok
  surface := len_a * len_b; -- ok
  len_sum := len_a * len_b; -- invalid
end Example1;
