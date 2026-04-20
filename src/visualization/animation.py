import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ── Sound (lazy init) ─────────────────────────────────────────────────────────
SOUND_ON = False
T_SPLIT = T_BASE = T_MERGE = T_DONE = T_PLOT = None

def _init_sound():
    global SOUND_ON, T_SPLIT, T_BASE, T_MERGE, T_DONE, T_PLOT
    try:
        import pygame
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        def _t(freq, dur, vol=0.4, sr=44100):
            t = np.linspace(0, dur, int(sr*dur), endpoint=False)
            w = (np.sin(2*np.pi*freq*t)*vol*32767).astype(np.int16)
            return pygame.sndarray.make_sound(w)
        T_SPLIT = _t(520, 0.12); T_BASE = _t(880, 0.10)
        T_MERGE = _t(330, 0.18); T_DONE  = _t(660, 0.30); T_PLOT = _t(440, 0.07)
        SOUND_ON = True
    except Exception:
        SOUND_ON = False

def _play(t):
    if SOUND_ON and t:
        try: t.play()
        except: pass

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = '#12122a'
PANEL_BG  = '#1a1a35'
TAB_ACT   = '#2a2a50'
ACCENT    = '#4a9eff'
BTN_PAUSE = '#e67e22'
BTN_RESET = '#555577'
C_DEF     = '#5B9BD5'
C_ACT     = '#FFC000'
C_MIN     = '#70AD47'
C_MAX     = '#FF4444'
C_DONE    = '#444466'
C_BASE_T  = '#aaaaff'
C_MERGE_T = '#ffcc66'
N_PEND    = '#2a2a50'
N_ACT     = '#FFC000'
N_DONE    = '#4a9eff'
EDGE_C    = '#555577'
WHITE     = '#ffffff'

# ── Country coordinates (lat, lon) ────────────────────────────────────────────
COORDS = {
    'Afghanistan':(33.9,67.7),'Albania':(41.2,20.2),'Algeria':(28.0,1.7),
    'Angola':(-11.2,17.9),'Argentina':(-38.4,-63.6),'Armenia':(40.1,45.0),
    'Australia':(-25.3,133.8),'Austria':(47.5,14.6),'Azerbaijan':(40.1,47.6),
    'Bahrain':(26.0,50.6),'Bangladesh':(23.7,90.4),'Belarus':(53.7,27.9),
    'Belgium':(50.5,4.5),'Bolivia':(-16.3,-63.6),'Bosnia':(43.9,17.7),
    'Brazil':(-14.2,-51.9),'Bulgaria':(42.7,25.5),'Cambodia':(12.6,104.9),
    'Cameroon':(3.8,11.5),'Canada':(56.1,-106.3),'Chile':(-35.7,-71.5),
    'China':(35.9,104.2),'Colombia':(4.6,-74.1),'Croatia':(45.1,15.2),
    'Cuba':(21.5,-79.5),'Czech Republic':(49.8,15.5),'Denmark':(56.3,9.5),
    'Ecuador':(-1.8,-78.2),'Egypt':(26.8,30.8),'Ethiopia':(9.1,40.5),
    'Finland':(61.9,25.7),'France':(46.2,2.2),'Germany':(51.2,10.5),
    'Ghana':(7.9,-1.0),'Greece':(39.1,21.8),'Guatemala':(15.8,-90.2),
    'Hungary':(47.2,19.5),'India':(20.6,78.9),'Indonesia':(-0.8,113.9),
    'Iran':(32.4,53.7),'Iraq':(33.2,43.7),'Ireland':(53.4,-8.2),
    'Israel':(31.0,34.9),'Italy':(41.9,12.6),'Japan':(36.2,138.3),
    'Jordan':(30.6,36.2),'Kazakhstan':(48.0,66.9),'Kenya':(-0.0,37.9),
    'Kuwait':(29.3,47.5),'Kyrgyzstan':(41.2,74.8),'Laos':(19.9,102.5),
    'Latvia':(56.9,24.6),'Lebanon':(33.9,35.9),'Libya':(26.3,17.2),
    'Lithuania':(55.2,23.9),'Luxembourg':(49.8,6.1),'Malaysia':(4.2,108.0),
    'Mali':(17.6,-2.0),'Mexico':(23.6,-102.6),'Moldova':(47.4,28.4),
    'Mongolia':(46.9,103.8),'Morocco':(31.8,-7.1),'Mozambique':(-18.7,35.5),
    'Myanmar':(21.9,95.9),'Nepal':(28.4,84.1),'Netherlands':(52.1,5.3),
    'New Zealand':(-40.9,174.9),'Nicaragua':(12.9,-85.2),'Niger':(17.6,8.1),
    'Nigeria':(9.1,8.7),'North Korea':(40.3,127.5),'Norway':(60.5,8.5),
    'Oman':(21.5,55.9),'Pakistan':(30.4,69.3),'Panama':(8.5,-80.8),
    'Paraguay':(-23.4,-58.4),'Peru':(-9.2,-75.0),'Philippines':(12.9,121.8),
    'Poland':(51.9,19.1),'Portugal':(39.4,-8.2),'Qatar':(25.4,51.2),
    'Romania':(45.9,24.9),'Russia':(61.5,105.3),'Saudi Arabia':(23.9,45.1),
    'Senegal':(14.5,-14.5),'Serbia':(44.0,21.0),'Sierra Leone':(8.5,-11.8),
    'Slovakia':(48.7,19.7),'Slovenia':(46.2,14.8),'Somalia':(5.2,46.2),
    'South Africa':(-30.6,22.9),'South Korea':(35.9,127.8),'Spain':(40.5,-3.7),
    'Sri Lanka':(7.9,80.8),'Sudan':(12.9,30.2),'Sweden':(60.1,18.6),
    'Switzerland':(46.8,8.2),'Syria':(34.8,38.9),'Taiwan':(23.7,121.0),
    'Tajikistan':(38.9,71.3),'Tanzania':(-6.4,34.9),'Thailand':(15.9,100.9),
    'Tunisia':(33.9,9.5),'Turkey':(38.9,35.2),'Turkmenistan':(38.9,59.6),
    'Uganda':(1.4,32.3),'Ukraine':(48.4,31.2),'United Arab Emirates':(23.4,53.8),
    'United Kingdom':(55.4,-3.4),'United States':(37.1,-95.7),'Uruguay':(-32.5,-55.8),
    'Uzbekistan':(41.4,64.6),'Venezuela':(6.4,-66.6),'Vietnam':(14.1,108.3),
    'Yemen':(15.6,48.5),'Zambia':(-13.1,27.8),'Zimbabwe':(-19.0,29.2),
}

# ── Algorithm helpers ─────────────────────────────────────────────────────────
def _collect_bar_steps(arr, l, r, steps):
    if l == r:
        steps.append({'action':'base_one','l':l,'r':r}); return arr[l],arr[l],l,l
    if r-l==1:
        mi,xi=(l,r) if arr[l]<=arr[r] else (r,l)
        steps.append({'action':'base_two','l':l,'r':r,'min_idx':mi,'max_idx':xi})
        return arr[mi],arr[xi],mi,xi
    mid=(l+r)//2
    steps.append({'action':'split','l':l,'r':r,'mid':mid})
    lmn,lmx,lmi,lxi=_collect_bar_steps(arr,l,mid,steps)
    rmn,rmx,rmi,rxi=_collect_bar_steps(arr,mid+1,r,steps)
    mn=lmn if lmn<rmn else rmn; mx=lmx if lmx>rmx else rmx
    mi=lmi if lmn<rmn else rmi; xi=lxi if lmx>rmx else rxi
    steps.append({'action':'merge','l':l,'r':r,'min_idx':mi,'max_idx':xi,'min_val':mn,'max_val':mx})
    return mn,mx,mi,xi

def _build_nodes(arr,l,r,depth,nodes,ctr):
    nid=ctr[0]; ctr[0]+=1
    nd={'id':nid,'l':l,'r':r,'depth':depth,'children':[],'min':None,'max':None,'x':0,'y':0}
    nodes.append(nd)
    if l==r or r-l==1: return nid
    mid=(l+r)//2
    li=_build_nodes(arr,l,mid,depth+1,nodes,ctr)
    ri=_build_nodes(arr,mid+1,r,depth+1,nodes,ctr)
    nd['children']=[li,ri]; return nid

def _collect_tree_frames(arr,l,r,frames,nmap):
    nd=next(n for n in nmap.values() if n['l']==l and n['r']==r)
    if l==r:
        frames.append({'id':nd['id'],'action':'base_one'}); return arr[l],arr[l]
    if r-l==1:
        frames.append({'id':nd['id'],'action':'base_two'})
        a,b=arr[l],arr[r]; return (a,b) if a<b else (b,a)
    frames.append({'id':nd['id'],'action':'split'})
    mid=(l+r)//2
    lmn,lmx=_collect_tree_frames(arr,l,mid,frames,nmap)
    rmn,rmx=_collect_tree_frames(arr,mid+1,r,frames,nmap)
    mn=lmn if lmn<rmn else rmn; mx=lmx if lmx>rmx else rmx
    frames.append({'id':nd['id'],'action':'merge','min_val':mn,'max_val':mx})
    return mn,mx

# ── Main App ──────────────────────────────────────────────────────────────────
class DivideConquerApp:
    TABS = ["Data Overview","D&C Animation","Recursion Tree","Performance","Comparisons","World Map"]

    def __init__(self, root, arr, perf_data=None, labels=None, full_data=None, full_labels=None):
        self.root        = root
        self.arr         = [round(v,2) for v in arr]
        self.n           = len(self.arr)
        self.labels      = labels or [f"Item_{i}" for i in range(self.n)]
        self.full_data   = [round(v,2) for v in (full_data or arr)]
        self.full_labels = full_labels or self.labels
        self.perf_data   = perf_data
        self._job        = None
        self._paused     = False
        self.active_tab  = 0
        self.tk_canvas   = None

        root.title("Divide & Conquer Min-Max Visualizer")
        root.configure(bg=BG)
        root.resizable(True, True)

        self._build_header()
        self._build_tabs()
        self._build_canvas()
        self._build_controls()
        self._draw_tab(0)

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill='x', pady=(8,0))
        tk.Label(f, text="Divide & Conquer Min-Max Visualizer",
                 font=('Courier',15,'bold'), bg=BG, fg=WHITE).pack()
        tk.Label(f, text="Weather Temperature Analysis  •  Divide & Conquer Algorithm",
                 font=('Courier',8), bg=BG, fg='#8888aa').pack()

    # ── Tab bar ───────────────────────────────────────────────────────────────
    def _build_tabs(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill='x', padx=8, pady=4)
        self.tab_btns = []
        for i, name in enumerate(self.TABS):
            b = tk.Button(f, text=name, font=('Courier',9,'bold'),
                          bg=PANEL_BG, fg=WHITE, relief='flat',
                          padx=10, pady=5, cursor='hand2',
                          command=lambda i=i: self._switch_tab(i))
            b.pack(side='left', padx=2)
            self.tab_btns.append(b)

    # ── Canvas area ───────────────────────────────────────────────────────────
    def _build_canvas(self):
        outer = tk.Frame(self.root, bg=PANEL_BG,
                         highlightbackground=ACCENT, highlightthickness=1)
        outer.pack(fill='both', expand=True, padx=8, pady=2)
        self.title_lbl = tk.Label(outer, text='', font=('Courier',12,'bold'),
                                  bg=PANEL_BG, fg=WHITE)
        self.title_lbl.pack(pady=(6,1))
        self.status_lbl = tk.Label(outer, text='Press  Run  to start',
                                   font=('Courier',9), bg=PANEL_BG, fg='#70AD47')
        self.status_lbl.pack()
        self.fig_frame = tk.Frame(outer, bg=PANEL_BG)
        self.fig_frame.pack(fill='both', expand=True)

    # ── Controls ──────────────────────────────────────────────────────────────
    def _build_controls(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill='x', padx=8, pady=5)

        self.run_btn = tk.Button(f, text='▶  Run', font=('Courier',10,'bold'),
                  bg=ACCENT, fg=WHITE, relief='flat', padx=14, pady=4,
                  cursor='hand2', command=self._run)
        self.run_btn.pack(side='left', padx=3)

        self.pause_btn = tk.Button(f, text='⏸  Pause', font=('Courier',10,'bold'),
                  bg=BTN_PAUSE, fg=WHITE, relief='flat', padx=14, pady=4,
                  cursor='hand2', command=self._toggle_pause, state='disabled')
        self.pause_btn.pack(side='left', padx=3)

        tk.Button(f, text='↺  Reset', font=('Courier',10,'bold'),
                  bg=BTN_RESET, fg=WHITE, relief='flat', padx=14, pady=4,
                  cursor='hand2', command=self._reset).pack(side='left', padx=3)

        tk.Label(f, text='Speed:', font=('Courier',9),
                 bg=BG, fg='#aaaacc').pack(side='left', padx=(14,3))

        # Speed buttons for precise control
        tk.Button(f, text='◀◀ Fast', font=('Courier',8), bg=PANEL_BG, fg=WHITE,
                  relief='flat', padx=6, pady=3, cursor='hand2',
                  command=lambda: self.speed_var.set(150)).pack(side='left', padx=2)

        self.speed_var = tk.IntVar(value=700)
        self.speed_slider = ttk.Scale(f, from_=100, to=2500, orient='horizontal',
                                      variable=self.speed_var, length=160)
        self.speed_slider.pack(side='left', padx=4)

        tk.Button(f, text='Slow ▶▶', font=('Courier',8), bg=PANEL_BG, fg=WHITE,
                  relief='flat', padx=6, pady=3, cursor='hand2',
                  command=lambda: self.speed_var.set(2500)).pack(side='left', padx=2)

        self.speed_lbl = tk.Label(f, text='700ms', font=('Courier',8),
                                  bg=BG, fg='#aaaacc', width=6)
        self.speed_lbl.pack(side='left', padx=2)

        def _update_lbl(*_):
            self.speed_lbl.config(text=f"{int(self.speed_var.get())}ms")
        self.speed_var.trace_add('write', _update_lbl)

    # ── Tab switching ─────────────────────────────────────────────────────────
    def _switch_tab(self, idx):
        self._stop()
        self._paused = False
        self.pause_btn.config(text='⏸  Pause', state='disabled')
        self.active_tab = idx
        self._draw_tab(idx)

    def _draw_tab(self, idx):
        for i, b in enumerate(self.tab_btns):
            b.config(bg=TAB_ACT if i==idx else PANEL_BG,
                     fg=ACCENT  if i==idx else WHITE)
        titles = [
            "Data Overview — All Countries & Temperatures",
            "D&C Animation — Array Split & Merge",
            "Recursion Tree — Node by Node",
            "Performance — Iterative vs Divide & Conquer",
            "Comparison Counts — Theoretical vs Actual",
            "World Map — Temperature by Country",
        ]
        self.title_lbl.config(text=titles[idx])
        self.status_lbl.config(text='Press  Run  to start', fg='#70AD47')
        for w in self.fig_frame.winfo_children():
            w.destroy()
        self.tk_canvas = None
        [self._setup_overview, self._setup_bar, self._setup_tree,
         self._setup_perf, self._setup_comparisons, self._setup_worldmap][idx]()

    # ── Tab 0: Data Overview (static) ─────────────────────────────────────────
    def _setup_overview(self):
        data, labels, n = self.full_data, self.full_labels, len(self.full_data)
        mn_val, mx_val = min(data), max(data)
        colors = [C_MIN if v==mn_val else C_MAX if v==mx_val else C_DEF for v in data]

        fig, ax = plt.subplots(figsize=(max(10, n*0.18), 5))
        fig.patch.set_facecolor(PANEL_BG); ax.set_facecolor(PANEL_BG)
        ax.bar(range(n), data, color=colors, edgecolor='white', linewidth=0.4)
        for i,(v,c) in enumerate(zip(data,colors)):
            if c in (C_MIN, C_MAX):
                off = 0.8 if v>=0 else -1.8
                ax.text(i, v+off, f"{labels[i]}\n{v}°C", ha='center',
                        va='bottom' if v>=0 else 'top', fontsize=7, color=WHITE,
                        fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=c, alpha=0.85, edgecolor='none'))
        ax.set_xticks(range(n))
        ax.set_xticklabels(labels, rotation=90, ha='center', fontsize=6, color=WHITE)
        ax.tick_params(colors=WHITE); ax.set_ylabel('Temperature (°C)', color='#aaaacc', fontsize=9)
        ax.axhline(0, color='#888899', linewidth=0.8, linestyle='--')
        for sp in ax.spines.values(): sp.set_edgecolor('#333355')
        mn_c = labels[data.index(mn_val)]; mx_c = labels[data.index(mx_val)]
        ax.legend(handles=[
            mpatches.Patch(color=C_MIN, label=f'Coldest: {mn_c} ({mn_val}°C)'),
            mpatches.Patch(color=C_MAX, label=f'Hottest: {mx_c} ({mx_val}°C)'),
            mpatches.Patch(color=C_DEF, label='Other countries'),
        ], loc='upper right', facecolor='#2a2a50', labelcolor=WHITE, fontsize=8)
        ax.set_title(f'All {n} Countries  |  Coldest: {mn_c} {mn_val}°C  |  Hottest: {mx_c} {mx_val}°C',
                     color=WHITE, fontsize=10, pad=8)
        fig.tight_layout(); self._embed(fig)
        self.status_lbl.config(text=f"{n} countries  |  Coldest: {mn_c} {mn_val}°C  |  Hottest: {mx_c} {mx_val}°C", fg='#70AD47')

    # ── Tab 1: D&C Bar animation ───────────────────────────────────────────────
    def _setup_bar(self):
        self.bar_steps = []; _collect_bar_steps(self.arr, 0, self.n-1, self.bar_steps)
        self.bar_idx = 0
        fig, ax = plt.subplots(figsize=(max(9, self.n*0.18), 4.5))
        fig.patch.set_facecolor(PANEL_BG); ax.set_facecolor(PANEL_BG)
        self.bars = ax.bar(range(self.n), self.arr, color=C_DEF, edgecolor='white', linewidth=0.4)
        ax.set_xticks(range(self.n))
        ax.set_xticklabels(self.labels, rotation=90, ha='center', fontsize=6, color=WHITE)
        ax.tick_params(colors=WHITE); ax.set_ylabel('Temperature (°C)', color='#aaaacc', fontsize=9)
        ax.axhline(0, color='#888899', linewidth=0.8, linestyle='--')
        for sp in ax.spines.values(): sp.set_edgecolor('#333355')
        ax.legend(handles=[
            mpatches.Patch(color=C_ACT, label='Active range'),
            mpatches.Patch(color=C_MIN, label='Min found'),
            mpatches.Patch(color=C_MAX, label='Max found'),
            mpatches.Patch(color=C_DONE, label='Processed'),
        ], loc='upper right', facecolor='#2a2a50', labelcolor=WHITE, fontsize=8)
        fig.tight_layout(); self._embed(fig)

    def _bar_step(self):
        if not self._alive(): return
        if self._paused: self._job = self.root.after(100, self._bar_step); return
        if self.bar_idx >= len(self.bar_steps):
            self._done('Done! Min & Max found.'); return
        step = self.bar_steps[self.bar_idx]; action = step['action']; l,r = step['l'],step['r']
        for i in range(l, r+1): self.bars[i].set_color(C_DONE)
        if action == 'split':
            _play(T_SPLIT)
            for i in range(l, r+1): self.bars[i].set_color(C_ACT)
            self.status_lbl.config(text=f"Split [{l}..{r}] → [{l}..{step['mid']}] | [{step['mid']+1}..{r}]", fg=C_ACT)
        elif action == 'base_one':
            _play(T_BASE); self.bars[l].set_color(C_MIN)
            self.status_lbl.config(text=f"Base(1) [{l}] {self.labels[l]} → min=max={self.arr[l]}°C", fg=C_MIN)
        elif action == 'base_two':
            _play(T_BASE)
            self.bars[step['min_idx']].set_color(C_MIN); self.bars[step['max_idx']].set_color(C_MAX)
            self.status_lbl.config(text=f"Base(2) [{l},{r}] → min={self.arr[step['min_idx']]}°C ({self.labels[step['min_idx']]})  max={self.arr[step['max_idx']]}°C ({self.labels[step['max_idx']]})", fg=C_BASE_T)
        elif action == 'merge':
            _play(T_MERGE)
            self.bars[step['min_idx']].set_color(C_MIN); self.bars[step['max_idx']].set_color(C_MAX)
            for i in range(l, r+1):
                if i not in (step['min_idx'], step['max_idx']): self.bars[i].set_color(C_DONE)
            self.status_lbl.config(text=f"Merge [{l}..{r}] → min={step['min_val']:.2f}°C  max={step['max_val']:.2f}°C", fg=C_MERGE_T)
        self.tk_canvas.draw(); self.bar_idx += 1
        self._job = self.root.after(int(self.speed_var.get()), self._bar_step)

    # ── Tab 2: Recursion Tree ─────────────────────────────────────────────────
    def _setup_tree(self):
        self.tree_nodes = []; _build_nodes(self.arr, 0, self.n-1, 0, self.tree_nodes, [0])
        self.nmap = {nd['id']: nd for nd in self.tree_nodes}
        self._assign_positions(self.tree_nodes[0]['id'], 0, [0])
        max_d = max(nd['depth'] for nd in self.tree_nodes)
        for nd in self.tree_nodes: nd['y'] = -nd['depth'] * 1.8
        all_x = [nd['x'] for nd in self.tree_nodes]
        all_y = [nd['y'] for nd in self.tree_nodes]
        self.tree_frames = []; _collect_tree_frames(self.arr, 0, self.n-1, self.tree_frames, self.nmap)
        self.tree_idx = 0; self.tree_visited = set()

        fig, ax = plt.subplots(figsize=(max(9,(max(all_x)-min(all_x)+2)*1.2), max(5,(max_d+1)*2.0)))
        fig.patch.set_facecolor(PANEL_BG); ax.set_facecolor(PANEL_BG); ax.axis('off')
        ax.set_xlim(min(all_x)-0.8, max(all_x)+0.8); ax.set_ylim(min(all_y)-0.8, 0.8)
        for nd in self.tree_nodes:
            for cid in nd['children']:
                ch = self.nmap[cid]
                ax.annotate('', xy=(ch['x'],ch['y']), xytext=(nd['x'],nd['y']),
                            arrowprops=dict(arrowstyle='->', color=EDGE_C, lw=1.5))
        self.node_circles = {}; self.node_texts = {}
        for nd in self.tree_nodes:
            c = plt.Circle((nd['x'],nd['y']), 0.45, color=N_PEND, zorder=2, ec='#aaaacc', lw=1.8)
            ax.add_patch(c); self.node_circles[nd['id']] = c
            t = ax.text(nd['x'], nd['y'], f"[{nd['l']}..{nd['r']}]",
                        ha='center', va='center', fontsize=7, color=WHITE, zorder=3, fontweight='bold')
            self.node_texts[nd['id']] = t
        ax.legend(handles=[mpatches.Patch(color=N_ACT,label='Active'),
                            mpatches.Patch(color=N_DONE,label='Resolved'),
                            mpatches.Patch(color=N_PEND,label='Pending')],
                  loc='upper right', facecolor='#2a2a50', labelcolor=WHITE, fontsize=8)
        fig.tight_layout(); self._embed(fig)

    def _assign_positions(self, nid, depth, counter):
        nd = self.nmap[nid]; nd['depth'] = depth
        if not nd['children']: nd['x'] = counter[0]; counter[0] += 1.3; return
        for cid in nd['children']: self._assign_positions(cid, depth+1, counter)
        nd['x'] = sum(self.nmap[c]['x'] for c in nd['children']) / len(nd['children'])

    def _tree_step(self):
        if not self._alive(): return
        if self._paused: self._job = self.root.after(100, self._tree_step); return
        for vid in self.tree_visited:
            vnd = self.nmap[vid]; self.node_circles[vid].set_color(N_DONE)
            if vnd.get('min') is not None:
                self.node_texts[vid].set_text(f"[{vnd['l']}..{vnd['r']}]\n{vnd['min']:.1f}/{vnd['max']:.1f}")
        if self.tree_idx >= len(self.tree_frames):
            self._done('Done! Tree fully resolved.'); self.tk_canvas.draw(); return
        event = self.tree_frames[self.tree_idx]; nid = event['id']; nd = self.nmap[nid]
        self.node_circles[nid].set_color(N_ACT); self.tree_visited.add(nid)
        if event['action'] == 'split':
            _play(T_SPLIT)
            self.status_lbl.config(text=f"Split [{nd['l']}..{nd['r']}] → left & right subtrees", fg=C_ACT)
        elif event['action'] == 'base_one':
            _play(T_BASE); nd['min'] = nd['max'] = self.arr[nd['l']]
            self.status_lbl.config(text=f"Base(1) [{nd['l']}] {self.labels[nd['l']]} → {self.arr[nd['l']]}°C", fg=C_MIN)
        elif event['action'] == 'base_two':
            _play(T_BASE); a,b = self.arr[nd['l']],self.arr[nd['r']]
            nd['min'],nd['max'] = (a,b) if a<b else (b,a)
            self.status_lbl.config(text=f"Base(2) [{nd['l']},{nd['r']}] → min={nd['min']:.2f}°C  max={nd['max']:.2f}°C", fg=C_BASE_T)
        elif event['action'] == 'merge':
            _play(T_MERGE); nd['min']=event['min_val']; nd['max']=event['max_val']
            self.status_lbl.config(text=f"Merge [{nd['l']}..{nd['r']}] → min={nd['min']:.2f}°C  max={nd['max']:.2f}°C", fg=C_MERGE_T)
        self.tk_canvas.draw(); self.tree_idx += 1
        self._job = self.root.after(int(self.speed_var.get()), self._tree_step)

    # ── Tab 3: Performance ────────────────────────────────────────────────────
    def _setup_perf(self):
        if not self.perf_data:
            tk.Label(self.fig_frame, text='No performance data.', bg=PANEL_BG,
                     fg='#aaaacc', font=('Courier',11)).pack(expand=True); return
        self.perf_sizes = self.perf_data['sizes']
        self.perf_iter  = self.perf_data['iter_times']
        self.perf_dc    = self.perf_data['dc_times']
        self.perf_idx   = 0
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor(PANEL_BG); ax.set_facecolor(PANEL_BG)
        ax.set_xlim(0, max(self.perf_sizes)*1.1)
        ax.set_ylim(0, max(max(self.perf_iter), max(self.perf_dc))*1.3)
        ax.set_xlabel('Input Size (n)', color='#aaaacc', fontsize=10)
        ax.set_ylabel('Execution Time (ms)', color='#aaaacc', fontsize=10)
        ax.set_title('Performance: Iterative vs Divide & Conquer', color=WHITE, fontsize=11)
        ax.tick_params(colors=WHITE); ax.grid(True, color='#333355', linewidth=0.5)
        for sp in ax.spines.values(): sp.set_edgecolor('#333355')
        self.perf_line_iter, = ax.plot([], [], 'o-', color='#4a9eff', lw=2, label='Iterative', ms=8)
        self.perf_line_dc,   = ax.plot([], [], 's-', color='#FF4444', lw=2, label='Divide & Conquer', ms=8)
        ax.legend(facecolor='#2a2a50', labelcolor=WHITE, fontsize=9)
        fig.tight_layout(); self._embed(fig)

    def _perf_step(self):
        if not self._alive(): return
        if self._paused: self._job = self.root.after(100, self._perf_step); return
        idx = self.perf_idx
        if idx > len(self.perf_sizes):
            self._done('Done! Performance comparison complete.'); return
        _play(T_PLOT)
        xs = self.perf_sizes[:idx]
        self.perf_line_iter.set_data(xs, self.perf_iter[:idx])
        self.perf_line_dc.set_data(xs, self.perf_dc[:idx])
        if idx > 0:
            n=self.perf_sizes[idx-1]; it=self.perf_iter[idx-1]; dc=self.perf_dc[idx-1]
            self.status_lbl.config(text=f"n={n}  Iterative={it:.3f}ms  D&C={dc:.3f}ms", fg=C_MERGE_T)
        self.tk_canvas.draw(); self.perf_idx += 1
        self._job = self.root.after(int(self.speed_var.get()), self._perf_step)

    # ── Tab 4: Comparisons ────────────────────────────────────────────────────
    def _setup_comparisons(self):
        from src.algorithms.iterative_min_max import find_min_max as iter_mm
        from src.algorithms.divide_conquer_min_max import DivideConquerMinMax as DC
        import random
        n_vals = [1,2,4,8,16,32,64,128,256,512,1024]
        ic,dc,th = [],[],[]
        for n in n_vals:
            a = [random.uniform(-30,50) for _ in range(n)]
            ic.append(iter_mm(a).comparisons); dc.append(DC.find_min_max(a).comparisons)
            th.append(max(0, int(1.5*n-2)))
        self.cmp_n=n_vals; self.cmp_iter=ic; self.cmp_dc=dc; self.cmp_theory=th; self.cmp_idx=0
        fig, ax = plt.subplots(figsize=(9,4.5))
        fig.patch.set_facecolor(PANEL_BG); ax.set_facecolor(PANEL_BG)
        ax.set_xlim(0, max(n_vals)*1.1); ax.set_ylim(0, max(max(ic),max(dc))*1.2)
        ax.set_xlabel('Input Size (n)', color='#aaaacc', fontsize=10)
        ax.set_ylabel('Comparisons', color='#aaaacc', fontsize=10)
        ax.set_title('Comparison Counts: Iterative vs D&C vs Theory (3n/2-2)', color=WHITE, fontsize=11)
        ax.tick_params(colors=WHITE); ax.grid(True, color='#333355', linewidth=0.5)
        for sp in ax.spines.values(): sp.set_edgecolor('#333355')
        self.cmp_li, = ax.plot([], [], 'o-', color='#4a9eff', lw=2, label='Iterative', ms=7)
        self.cmp_ld, = ax.plot([], [], 's-', color='#FF4444', lw=2, label='D&C actual', ms=7)
        self.cmp_lt, = ax.plot([], [], '--', color='#70AD47', lw=2, label='Theory 3n/2-2', ms=5)
        ax.legend(facecolor='#2a2a50', labelcolor=WHITE, fontsize=9)
        fig.tight_layout(); self._embed(fig)

    def _cmp_step(self):
        if not self._alive(): return
        if self._paused: self._job = self.root.after(100, self._cmp_step); return
        idx = self.cmp_idx
        if idx > len(self.cmp_n):
            self._done('Done! D&C matches theory 3n/2-2 exactly.'); return
        _play(T_PLOT)
        xs = self.cmp_n[:idx]
        self.cmp_li.set_data(xs, self.cmp_iter[:idx])
        self.cmp_ld.set_data(xs, self.cmp_dc[:idx])
        self.cmp_lt.set_data(xs, self.cmp_theory[:idx])
        if idx > 0:
            n=self.cmp_n[idx-1]
            self.status_lbl.config(text=f"n={n}  Iterative={self.cmp_iter[idx-1]}  D&C={self.cmp_dc[idx-1]}  Theory={self.cmp_theory[idx-1]}", fg=C_MERGE_T)
        self.tk_canvas.draw(); self.cmp_idx += 1
        self._job = self.root.after(int(self.speed_var.get()), self._cmp_step)

    # ── Tab 5: World Map (static) ─────────────────────────────────────────────
    def _setup_worldmap(self):
        # Build dataset: prefer full_data/full_labels if they match COORDS,
        # otherwise fall back to the entire built-in COORDS dictionary
        lats, lons, temps, names = [], [], [], []
        for label, temp in zip(self.full_labels, self.full_data):
            if label in COORDS:
                lat, lon = COORDS[label]
                lats.append(lat); lons.append(lon)
                temps.append(temp); names.append(label)

        # If nothing matched, use ALL built-in COORDS with default temperatures
        if not lats:
            default_temps = {
                'Afghanistan':22.5,'Albania':12.3,'Algeria':25.1,'Angola':24.8,
                'Argentina':14.2,'Armenia':8.7,'Australia':21.3,'Austria':7.4,
                'Azerbaijan':11.2,'Bahrain':28.9,'Bangladesh':25.6,'Belarus':5.8,
                'Belgium':9.1,'Bolivia':15.3,'Bosnia':9.8,'Brazil':24.7,
                'Bulgaria':10.2,'Cambodia':27.4,'Cameroon':24.1,'Canada':-5.3,
                'Chile':12.8,'China':11.4,'Colombia':18.2,'Croatia':11.5,
                'Cuba':25.3,'Czech Republic':8.3,'Denmark':7.2,'Ecuador':17.5,
                'Egypt':22.8,'Ethiopia':16.4,'Finland':1.2,'France':11.3,
                'Germany':8.5,'Ghana':26.8,'Greece':15.7,'Guatemala':19.2,
                'Hungary':9.7,'India':24.5,'Indonesia':26.3,'Iran':17.2,
                'Iraq':22.4,'Ireland':9.3,'Israel':19.8,'Italy':13.2,
                'Japan':12.4,'Jordan':18.6,'Kazakhstan':5.1,'Kenya':19.3,
                'Kuwait':26.7,'Kyrgyzstan':3.2,'Laos':23.8,'Latvia':5.6,
                'Lebanon':16.4,'Libya':21.3,'Lithuania':5.9,'Luxembourg':8.7,
                'Malaysia':27.1,'Mali':28.4,'Mexico':18.7,'Moldova':8.4,
                'Mongolia':-0.7,'Morocco':17.5,'Mozambique':24.2,'Myanmar':24.6,
                'Nepal':9.8,'Netherlands':9.4,'New Zealand':12.1,'Nicaragua':25.3,
                'Niger':29.1,'Nigeria':26.5,'North Korea':8.2,'Norway':1.8,
                'Oman':27.4,'Pakistan':20.3,'Panama':26.1,'Paraguay':22.4,
                'Peru':15.8,'Philippines':26.9,'Poland':7.8,'Portugal':15.4,
                'Qatar':28.2,'Romania':9.3,'Russia':-5.1,'Saudi Arabia':25.8,
                'Senegal':27.3,'Serbia':10.4,'Sierra Leone':26.2,'Slovakia':8.1,
                'Slovenia':9.6,'Somalia':27.8,'South Africa':17.2,'South Korea':11.3,
                'Spain':14.8,'Sri Lanka':27.4,'Sudan':28.7,'Sweden':2.4,
                'Switzerland':5.3,'Syria':17.1,'Taiwan':22.3,'Tajikistan':4.7,
                'Tanzania':22.1,'Thailand':27.2,'Tunisia':18.4,'Turkey':11.8,
                'Turkmenistan':12.4,'Uganda':21.3,'Ukraine':7.2,
                'United Arab Emirates':27.6,'United Kingdom':9.2,
                'United States':8.5,'Uruguay':14.7,'Uzbekistan':11.3,
                'Venezuela':24.8,'Vietnam':23.4,'Yemen':25.6,'Zambia':20.4,'Zimbabwe':19.8,
            }
            for country, (lat, lon) in COORDS.items():
                lats.append(lat); lons.append(lon)
                temps.append(default_temps.get(country, 15.0))
                names.append(country)

        self._draw_worldmap(lats, lons, temps, names)

    def _draw_worldmap(self, lats, lons, temps, names):
        fig, ax = plt.subplots(figsize=(14, 7))
        fig.patch.set_facecolor('#0a1628')
        ax.set_facecolor('#1a3a5c')  # ocean color

        # ── Draw land using simplified continent polygons ──────────────────
        import matplotlib.patches as mpatches_poly
        from matplotlib.patches import Polygon as MplPolygon
        from matplotlib.collections import PatchCollection

        # Simplified continent outlines as (lon, lat) polygons
        continents = [
            # North America
            [(-168,72),(-140,70),(-120,60),(-100,50),(-80,45),(-70,47),(-60,47),
             (-55,50),(-53,47),(-60,44),(-65,44),(-70,42),(-75,35),(-80,25),
             (-85,20),(-90,15),(-85,10),(-78,8),(-77,8),(-80,10),(-83,10),
             (-88,15),(-92,18),(-97,20),(-105,22),(-110,23),(-117,32),(-120,35),
             (-124,40),(-130,55),(-140,60),(-155,60),(-165,65),(-168,72)],
            # South America
            [(-80,10),(-75,12),(-62,12),(-60,8),(-52,5),(-50,0),(-48,-5),
             (-35,-8),(-35,-15),(-38,-20),(-40,-22),(-43,-23),(-45,-25),
             (-48,-28),(-52,-33),(-58,-38),(-62,-42),(-65,-45),(-68,-50),
             (-68,-55),(-65,-55),(-63,-52),(-58,-48),(-55,-45),(-52,-42),
             (-50,-28),(-48,-25),(-45,-22),(-42,-20),(-40,-15),(-38,-10),
             (-50,-5),(-55,0),(-60,5),(-65,8),(-72,10),(-80,10)],
            # Europe
            [(-10,36),(-8,38),(-9,42),(-8,44),(-2,44),(3,44),(5,43),(8,44),
             (12,44),(14,45),(16,46),(18,45),(20,44),(22,42),(26,42),(28,42),
             (30,46),(32,48),(30,50),(28,54),(24,56),(20,58),(18,60),(16,62),
             (14,65),(18,70),(25,72),(30,70),(28,65),(30,60),(32,58),(28,56),
             (24,54),(20,54),(18,56),(14,58),(10,58),(8,56),(5,54),(2,52),
             (0,50),(-2,48),(-5,48),(-8,44),(-10,40),(-10,36)],
            # Africa
            [(-18,15),(-15,12),(-12,10),(-10,8),(-8,5),(-5,5),(-2,5),
             (2,5),(5,5),(8,4),(10,2),(12,0),(14,-2),(16,-5),(18,-8),
             (20,-12),(22,-18),(24,-22),(26,-25),(28,-30),(30,-35),(32,-30),
             (34,-25),(36,-20),(38,-15),(40,-10),(42,-5),(44,0),(46,5),
             (44,10),(42,12),(40,15),(38,18),(36,22),(34,25),(32,28),
             (30,30),(28,32),(25,35),(20,37),(15,37),(10,37),(5,37),
             (0,35),(-5,35),(-10,32),(-15,28),(-18,22),(-18,15)],
            # Asia
            [(26,42),(30,46),(35,48),(40,50),(45,52),(50,55),(55,58),(60,60),
             (65,62),(70,65),(75,68),(80,72),(85,75),(90,75),(95,72),(100,70),
             (105,68),(110,65),(115,60),(120,55),(125,50),(130,45),(135,42),
             (138,38),(140,35),(142,30),(140,25),(138,20),(135,15),(130,10),
             (125,5),(120,2),(115,0),(110,-5),(105,-8),(100,-5),(95,5),
             (90,10),(85,15),(80,20),(75,25),(70,22),(65,25),(60,22),
             (55,25),(50,28),(45,30),(40,35),(35,38),(30,40),(26,42)],
            # Australia
            [(114,-22),(116,-20),(118,-18),(122,-18),(126,-18),(130,-15),
             (132,-12),(136,-12),(138,-15),(140,-18),(142,-20),(144,-22),
             (146,-25),(148,-28),(150,-30),(152,-32),(154,-28),(152,-25),
             (150,-22),(148,-20),(146,-18),(144,-15),(142,-12),(140,-10),
             (138,-12),(136,-15),(134,-18),(132,-20),(130,-22),(128,-25),
             (126,-28),(124,-30),(122,-32),(120,-30),(118,-28),(116,-25),(114,-22)],
            # Greenland
            [(-45,60),(-42,65),(-40,70),(-38,75),(-35,78),(-30,80),(-25,82),
             (-20,83),(-15,82),(-10,80),(-15,78),(-20,75),(-25,72),(-30,70),
             (-35,68),(-40,65),(-45,62),(-45,60)],
        ]

        land_patches = []
        for poly in continents:
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            patch = MplPolygon(list(zip(xs, ys)), closed=True)
            land_patches.append(patch)

        land_col = PatchCollection(land_patches, facecolor='#2d4a2d',
                                   edgecolor='#3a5a3a', linewidth=0.6, zorder=1)
        ax.add_collection(land_col)

        # ── Grid and axes ──────────────────────────────────────────────────
        ax.set_xlim(-180, 180); ax.set_ylim(-90, 90)
        ax.set_xlabel('Longitude', color='#aaaacc', fontsize=8)
        ax.set_ylabel('Latitude',  color='#aaaacc', fontsize=8)
        ax.tick_params(colors='#aaaacc', labelsize=7)
        for sp in ax.spines.values(): sp.set_edgecolor('#334466')
        for lat in range(-90, 91, 30):
            ax.axhline(lat, color='#1a3a5c', lw=0.5, zorder=0)
        for lon in range(-180, 181, 30):
            ax.axvline(lon, color='#1a3a5c', lw=0.5, zorder=0)
        ax.axhline(0, color='#2255aa', lw=0.8, ls='--', zorder=2, alpha=0.6)
        ax.axvline(0, color='#2255aa', lw=0.8, ls='--', zorder=2, alpha=0.6)

        # ── Scatter countries ──────────────────────────────────────────────
        cmap = plt.cm.RdYlBu_r
        norm = mcolors.Normalize(vmin=min(self.full_data), vmax=max(self.full_data))
        sc = ax.scatter(lons, lats, c=temps, cmap=cmap, norm=norm,
                        s=140, zorder=5, edgecolors='white', linewidths=0.8, alpha=0.95)

        # Label every country dot
        for lon, lat, name, temp in zip(lons, lats, names, temps):
            ax.annotate(f"{name}\n{temp}°C", xy=(lon, lat), xytext=(4, 4),
                        textcoords='offset points', fontsize=5.5, color='white', zorder=6,
                        bbox=dict(boxstyle='round,pad=0.15', facecolor='#0a1628',
                                  alpha=0.75, edgecolor='none'))

        # Highlight min and max
        mn_val, mx_val = min(temps), max(temps)
        for lon, lat, name, temp in zip(lons, lats, names, temps):
            if temp == mn_val:
                ax.scatter(lon, lat, s=350, c='#4a9eff', zorder=7, edgecolors='white', lw=2)
                ax.annotate(f"COLDEST\n{name}\n{temp}°C",
                            xy=(lon, lat), xytext=(12, 10), textcoords='offset points',
                            fontsize=8, color='#4a9eff', fontweight='bold', zorder=8,
                            bbox=dict(boxstyle='round,pad=0.35', facecolor='#0a1628',
                                      alpha=0.92, edgecolor='#4a9eff', lw=1.5))
            if temp == mx_val:
                ax.scatter(lon, lat, s=350, c='#FF4444', zorder=7, edgecolors='white', lw=2)
                ax.annotate(f"HOTTEST\n{name}\n{temp}°C",
                            xy=(lon, lat), xytext=(12, -24), textcoords='offset points',
                            fontsize=8, color='#FF4444', fontweight='bold', zorder=8,
                            bbox=dict(boxstyle='round,pad=0.35', facecolor='#0a1628',
                                      alpha=0.92, edgecolor='#FF4444', lw=1.5))

        # Colorbar
        cbar = fig.colorbar(sc, ax=ax, orientation='vertical', fraction=0.018, pad=0.02)
        cbar.set_label('Temperature (°C)', color='white', fontsize=9)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white', fontsize=8)

        mn_c = names[temps.index(mn_val)]; mx_c = names[temps.index(mx_val)]
        ax.set_title(
            f'World Temperature Map — {len(names)} countries  |  '
            f'❄ Coldest: {mn_c} ({mn_val}°C)  |  🔥 Hottest: {mx_c} ({mx_val}°C)',
            color='white', fontsize=10, pad=10)

        fig.tight_layout(); self._embed(fig)
        self.status_lbl.config(
            text=f"{len(names)} countries on map  |  Blue=cold  Red=hot  |  Green=land  Blue=ocean",
            fg='#70AD47')

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _embed(self, fig):
        self.fig = fig
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        self.tk_canvas = canvas

    def _alive(self):
        try: return self.root.winfo_exists()
        except: return False

    def _done(self, msg):
        _play(T_DONE)
        self.status_lbl.config(text=msg, fg=C_MIN)
        self.pause_btn.config(state='disabled')
        self._paused = False

    def _run(self):
        self._stop(); self._paused = False
        self.pause_btn.config(text='⏸  Pause', state='normal')
        self.status_lbl.config(text='Running...', fg='#aaaaff')
        t = self.active_tab
        if t == 0:
            self._setup_overview()
        elif t == 1:
            self.bar_idx = 0
            for b in self.bars: b.set_color(C_DEF)
            self.tk_canvas.draw()
            self._job = self.root.after(300, self._bar_step)
        elif t == 2:
            self.tree_idx = 0; self.tree_visited = set()
            for nd in self.tree_nodes:
                self.node_circles[nd['id']].set_color(N_PEND)
                self.node_texts[nd['id']].set_text(f"[{nd['l']}..{nd['r']}]")
                nd['min'] = nd['max'] = None
            self.tk_canvas.draw()
            self._job = self.root.after(300, self._tree_step)
        elif t == 3:
            if self.perf_data:
                self.perf_idx = 0
                self.perf_line_iter.set_data([], []); self.perf_line_dc.set_data([], [])
                self.tk_canvas.draw()
                self._job = self.root.after(300, self._perf_step)
        elif t == 4:
            self.cmp_idx = 0
            self.cmp_li.set_data([], []); self.cmp_ld.set_data([], []); self.cmp_lt.set_data([], [])
            self.tk_canvas.draw()
            self._job = self.root.after(300, self._cmp_step)
        else:
            self._setup_worldmap()
            self.pause_btn.config(state='disabled')

    def _toggle_pause(self):
        self._paused = not self._paused
        if self._paused:
            self.pause_btn.config(text='▶  Resume')
            self.status_lbl.config(text='Paused — press Resume to continue', fg=BTN_PAUSE)
        else:
            self.pause_btn.config(text='⏸  Pause')
            self.status_lbl.config(text='Running...', fg='#aaaaff')

    def _reset(self):
        self._stop(); self._paused = False
        self.pause_btn.config(text='⏸  Pause', state='disabled')
        self._draw_tab(self.active_tab)

    def _stop(self):
        if self._job:
            try: self.root.after_cancel(self._job)
            except: pass
            self._job = None


# ── Entry point ───────────────────────────────────────────────────────────────
def animate(arr, perf_data=None, labels=None, full_data=None, full_labels=None):
    _init_sound()
    root = tk.Tk()
    root.geometry("1150x700")
    root.configure(bg=BG)
    DivideConquerApp(root, arr, perf_data=perf_data, labels=labels,
                     full_data=full_data, full_labels=full_labels)
    root.mainloop()

def animate_tree(arr):
    pass
