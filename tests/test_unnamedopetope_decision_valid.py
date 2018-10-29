from UnnamedOpetope import address, ProofTree

p = ProofTree({
    address([], 2): {
        address([], 1): {
            address('*'): {}  # {} represents the point
        },
        address(['*']): {
            address('*'): {}
        }
    },
    address([['*']]): {
        None: {}  # indicates a degeneracy
    }})

print(p)
print()
print(p.eval())
