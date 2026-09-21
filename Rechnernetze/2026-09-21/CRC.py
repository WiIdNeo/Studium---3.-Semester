def xor(a, b):
    output = ""
    for i in range(len(a)):
        if int(a[i]) + int(b[i]) == 2 or int(a[i]) + int(b[i]) == 0:
            output += "0"
        else:
            output += "1"
    return output

message = "1001010110101010110111111010111010101011101011110110100"
message_ = message
polynom = "1011"
k = len(polynom)

for i in range(k-1):
    message_ += "0"

calc = message_[0:k-1]
j = k-1
while j < len(message_):
    calc = calc + message_[j]
    if calc[0] == "1":
        calc = xor(calc, polynom)
    calc = calc[1:]
    j += 1
crc = calc

message_2_send = message + crc

print(f"Sender")
print(f"Message: {message}")
print(f"CRC: {crc}")
print(f"Bitchain to send: {message_2_send}")
print("")
#message_2_send = message_2_send[:3] + ("1" if message_2_send[3] == "0" else "0") + message_2_send[4:]
print("Reciver:")
print(f"Recived Bit chain: {message_2_send}")

calc = message_2_send[0:k-1]
j = k-1
while j < len(message_2_send):
    calc = calc + message_2_send[j]
    if calc[0] == "1":
        calc = xor(calc, polynom)
    calc = calc[1:]
    j += 1

if "1" in calc:
    print("Tranfered with errors")
else:
    print("correctly transferred")
    message_recived = message_2_send[:-(len(polynom)-1)]
    print(f"Message: {message_recived}")

