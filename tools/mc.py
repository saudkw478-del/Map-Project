"""Small helpers for generating Minecraft command lists (+ a voxel copy for previews)."""

LIMIT = 30000  # vanilla /fill cap is 32768 blocks


def rel(v):
    return "~" if v == 0 else f"~{v}"


def _split(x1, y1, z1, x2, y2, z2):
    dx, dy, dz = x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1
    if dx * dy * dz <= LIMIT:
        yield (x1, y1, z1, x2, y2, z2)
        return
    if dx >= dy and dx >= dz:
        m = (x1 + x2) // 2
        yield from _split(x1, y1, z1, m, y2, z2)
        yield from _split(m + 1, y1, z1, x2, y2, z2)
    elif dz >= dy:
        m = (z1 + z2) // 2
        yield from _split(x1, y1, z1, x2, y2, m)
        yield from _split(x1, y1, m + 1, x2, y2, z2)
    else:
        m = (y1 + y2) // 2
        yield from _split(x1, y1, z1, x2, m, z2)
        yield from _split(x1, m + 1, z1, x2, y2, z2)


class Build:
    """Collects relative-coordinate commands. Coordinates are offsets from the origin marker."""
    KEEP_AIR = False   # world builder sets True so carved air really clears terrain

    def __init__(self, preview=True):
        self.cmds = []
        self.vox = {}
        self.chests = []   # (x, y, z, loot table name)
        self.preview = preview

    def raw(self, cmd):
        self.cmds.append(cmd)

    def set(self, x, y, z, block):
        self.cmds.append(f"setblock {rel(x)} {rel(y)} {rel(z)} {block}")
        if self.preview:
            self._vox(x, y, z, block)

    def fill(self, x1, y1, z1, x2, y2, z2, block):
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        z1, z2 = sorted((z1, z2))
        for a, b, c, d, e, f in _split(x1, y1, z1, x2, y2, z2):
            self.cmds.append(f"fill {rel(a)} {rel(b)} {rel(c)} {rel(d)} {rel(e)} {rel(f)} {block}")
        if self.preview:
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    for z in range(z1, z2 + 1):
                        self._vox(x, y, z, block)

    def chest(self, x, y, z, facing, table):
        self.set(x, y, z, f"chest[facing={facing}]")
        self.chests.append((x, y, z, table))

    def _vox(self, x, y, z, block):
        if block == "air" and not Build.KEEP_AIR:
            self.vox.pop((x, y, z), None)
        else:
            self.vox[(x, y, z)] = block

    def chunk(self, size):
        """Split the command list into pieces of at most `size` commands."""
        return [self.cmds[i:i + size] for i in range(0, len(self.cmds), size)]
