import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import random
from simulation.person import Person
from simulation.simclass import Simulation
from simulation.rumor import Rumor
from simulation.settings import *

def create_demo_people():
    people = []
    
    # Create people with different personalities
    alice = Person(name="Alice", mbti="ENFJ", gullibility=300, gossip_level=800)
    bob = Person(name="Bob", mbti="ISTP", anger=200, convo_stay=700)
    charlie = Person(name="Charlie", mbti="ENTP", gullibility=600, gossip_level=400)
    dave = Person(name="Dave", mbti="INTJ", anger=100, convo_stay=300)
    
    people.extend([alice, bob, charlie, dave])
    return people

def create_demo_rumors(people):
    rumors = []
    
    # Create some juicy rumors
    rumors.append(Rumor(
        text="Alice secretly hates Dave's cooking",
        plausibility=700,
        harmfulness=300,
        subjects=[people[3]],  # Dave
        originators=[people[0]]  # Alice
    ))
    
    rumors.append(Rumor(
        text="Bob cheated on his last test",
        plausibility=400,
        harmfulness=600,
        subjects=[people[1]],  # Bob
        originators=[people[2]]  # Charlie
    ))
    
    rumors.append(Rumor(
        text="Charlie is planning to quit his job",
        plausibility=500,
        harmfulness=400,
        subjects=[people[2]],  # Charlie
        originators=[people[1]]  # Bob
    ))
    
    return rumors

class SimulationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Party Fight Instigator - Simulation")
        self.master.geometry("1400x900")
        self.master.configure(bg="#2b2b2b")
        
        # Create simulation
        people = create_demo_people()
        self.sim = Simulation(people=people, min_convos=1, max_convos=2)
        
        # Add rumors to people
        rumors = create_demo_rumors(people)
        for rumor in rumors:
            rumor.originators[0].rumors.add(rumor)
        
        self.tick_count = 0
        self.setup_gui()
        self.update_display()
        
    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create main horizontal layout with three sections
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Left panel - NPCs and controls
        self.setup_left_panel(left_frame)
        
        # Center panel - Player Relationships
        self.setup_center_panel(center_frame)
        
        # Right panel - Output and chat
        self.setup_right_panel(right_frame)
        
        # Initial output
        self.log_output("🎉 Simulation started!")
        self.log_output("=" * 50)
        
    def setup_left_panel(self, parent):
        # Control buttons frame
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Simulation tick button
        self.tick_button = ttk.Button(
            controls_frame, 
            text="🎯 Simulation Tick", 
            command=self.simulation_tick,
            style="Accent.TButton"
        )
        self.tick_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Tick counter label
        self.tick_label = ttk.Label(controls_frame, text="Tick: 0", font=("Arial", 12, "bold"))
        self.tick_label.pack(side=tk.LEFT)
        
        # NPCs frame
        npcs_frame = ttk.LabelFrame(parent, text="NPCs", padding=10)
        npcs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for NPC tabs
        self.npc_notebook = ttk.Notebook(npcs_frame)
        self.npc_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for each NPC
        self.npc_frames = {}
        for person in self.sim.people.values():
            self.create_npc_tab(person)
    
    def setup_center_panel(self, parent):
        # Player relationships frame
        relationships_frame = ttk.LabelFrame(parent, text="Your Relationships", padding=10)
        relationships_frame.pack(fill=tk.BOTH, expand=True)
        relationships_frame.configure(width=300)
        
        # Create a canvas and scrollbar for the relationships
        canvas_frame = ttk.Frame(relationships_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.rel_canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", width=280)
        rel_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.rel_canvas.yview)
        self.rel_scrollable_frame = ttk.Frame(self.rel_canvas)
        
        self.rel_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.rel_canvas.configure(scrollregion=self.rel_canvas.bbox("all"))
        )
        
        self.rel_canvas.create_window((0, 0), window=self.rel_scrollable_frame, anchor="nw")
        self.rel_canvas.configure(yscrollcommand=rel_scrollbar.set)
        
        self.rel_canvas.pack(side="left", fill="both", expand=True)
        rel_scrollbar.pack(side="right", fill="y")
        
        # Create relationship widgets for each NPC
        self.relationship_widgets = {}
        self.create_relationship_widgets()
    
    def setup_right_panel(self, parent):
        # Output frame
        output_frame = ttk.LabelFrame(parent, text="Simulation Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.WORD, 
            height=20,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Chat frame
        chat_frame = ttk.LabelFrame(parent, text="Chat with NPCs", padding=10)
        chat_frame.pack(fill=tk.X, pady=(5, 0))
        
        # NPC selection for chat
        chat_controls_frame = ttk.Frame(chat_frame)
        chat_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(chat_controls_frame, text="Talk to:").pack(side=tk.LEFT)
        
        self.selected_npc = tk.StringVar()
        self.npc_combo = ttk.Combobox(
            chat_controls_frame, 
            textvariable=self.selected_npc,
            values=[person.name for person in self.sim.people.values()],
            state="readonly",
            width=15
        )
        self.npc_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.npc_combo.current(0)
        
        # Message input
        message_frame = ttk.Frame(chat_frame)
        message_frame.pack(fill=tk.X)
        
        self.message_entry = ttk.Entry(message_frame, font=("Arial", 11))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        self.send_button = ttk.Button(
            message_frame, 
            text="💬 Send", 
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
        
    def create_relationship_widgets(self):
        """Create widgets for displaying player relationships with each NPC"""
        for person in self.sim.people.values():
            # Create frame for this relationship
            rel_frame = ttk.LabelFrame(self.rel_scrollable_frame, text=person.name, padding=8)
            rel_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Get player conversation data
            player_convo = self.sim.get_player_conversation(person.id)
            
            # Trust label
            trust_frame = ttk.Frame(rel_frame)
            trust_frame.pack(fill=tk.X, pady=2)
            trust_label = ttk.Label(trust_frame, text="🤝 Trust:", font=("Arial", 9, "bold"))
            trust_label.pack(side=tk.LEFT)
            trust_value = ttk.Label(trust_frame, font=("Arial", 9))
            trust_value.pack(side=tk.RIGHT)
            
            # Animosity label
            animosity_frame = ttk.Frame(rel_frame)
            animosity_frame.pack(fill=tk.X, pady=2)
            animosity_label = ttk.Label(animosity_frame, text="😠 Animosity:", font=("Arial", 9, "bold"))
            animosity_label.pack(side=tk.LEFT)
            animosity_value = ttk.Label(animosity_frame, font=("Arial", 9))
            animosity_value.pack(side=tk.RIGHT)
            
            # NPC Anger label
            anger_frame = ttk.Frame(rel_frame)
            anger_frame.pack(fill=tk.X, pady=2)
            anger_label = ttk.Label(anger_frame, text="🔥 Their Anger:", font=("Arial", 9, "bold"))
            anger_label.pack(side=tk.LEFT)
            anger_value = ttk.Label(anger_frame, font=("Arial", 9))
            anger_value.pack(side=tk.RIGHT)
            
            # Store references for updating
            self.relationship_widgets[person.id] = {
                'trust': trust_value,
                'animosity': animosity_value,
                'anger': anger_value
            }
    
    def create_npc_tab(self, person):
        # Create tab frame
        tab_frame = ttk.Frame(self.npc_notebook)
        self.npc_notebook.add(tab_frame, text=person.name)
        self.npc_frames[person.id] = tab_frame
        
        # Main info frame
        info_frame = ttk.Frame(tab_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Basic info
        basic_frame = ttk.LabelFrame(info_frame, text="Basic Info", padding=10)
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        basic_info = f"""
Name: {person.name}
MBTI: {person.mbti}
ID: {person.id}
        """.strip()
        
        basic_label = ttk.Label(basic_frame, text=basic_info, font=("Arial", 10))
        basic_label.pack(anchor=tk.W)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(info_frame, text="Current Stats", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create labels for dynamic stats
        setattr(self, f"anger_label_{person.id}", ttk.Label(stats_frame, font=("Arial", 10)))
        setattr(self, f"gullibility_label_{person.id}", ttk.Label(stats_frame, font=("Arial", 10)))
        setattr(self, f"gossip_label_{person.id}", ttk.Label(stats_frame, font=("Arial", 10)))
        setattr(self, f"convo_label_{person.id}", ttk.Label(stats_frame, font=("Arial", 10)))
        
        getattr(self, f"anger_label_{person.id}").pack(anchor=tk.W)
        getattr(self, f"gullibility_label_{person.id}").pack(anchor=tk.W)
        getattr(self, f"gossip_label_{person.id}").pack(anchor=tk.W)
        getattr(self, f"convo_label_{person.id}").pack(anchor=tk.W)
        
        # Rumors frame
        rumors_frame = ttk.LabelFrame(info_frame, text="Known Rumors", padding=10)
        rumors_frame.pack(fill=tk.BOTH, expand=True)
        
        # Rumors text area
        rumors_text = scrolledtext.ScrolledText(
            rumors_frame, 
            wrap=tk.WORD, 
            height=8,
            font=("Arial", 9),
            bg="#f0f0f0"
        )
        rumors_text.pack(fill=tk.BOTH, expand=True)
        setattr(self, f"rumors_text_{person.id}", rumors_text)
        
    def update_display(self):
        # Update tick counter
        self.tick_label.config(text=f"Tick: {self.tick_count}")
        
        # Update each NPC tab
        for person in self.sim.people.values():
            # Update stats
            anger_color = "🔥" if person.anger > 500 else "😊" if person.anger < 200 else "😐"
            getattr(self, f"anger_label_{person.id}").config(
                text=f"{anger_color} Anger: {person.anger}/1000"
            )
            getattr(self, f"gullibility_label_{person.id}").config(
                text=f"🤔 Gullibility: {person.gullibility}/1000"
            )
            getattr(self, f"gossip_label_{person.id}").config(
                text=f"💬 Gossip Level: {person.gossip_level}/1000"
            )
            
            convo_status = "In conversation" if person.active_conversation else "Available"
            convo_icon = "👥" if person.active_conversation else "🚶"
            getattr(self, f"convo_label_{person.id}").config(
                text=f"{convo_icon} Status: {convo_status}"
            )
            
            # Update rumors
            rumors_widget = getattr(self, f"rumors_text_{person.id}")
            rumors_widget.delete(1.0, tk.END)
            
            if person.rumors:
                for i, rumor in enumerate(person.rumors, 1):
                    rumors_widget.insert(tk.END, f"{i}. {rumor.text}\n")
                    rumors_widget.insert(tk.END, f"   Plausibility: {rumor.plausibility}, Harmfulness: {rumor.harmfulness}\n\n")
            else:
                rumors_widget.insert(tk.END, "No rumors known yet...")
        
        # Update player relationships
        self.update_relationship_display()
    
    def update_relationship_display(self):
        """Update the player relationship display"""
        for person_id, widgets in self.relationship_widgets.items():
            player_convo = self.sim.get_player_conversation(person_id)
            person = self.sim.people[person_id]
            
            if player_convo:
                # Color coding for trust levels
                trust_color = "green" if player_convo.trust > 600 else "orange" if player_convo.trust > 300 else "red"
                widgets['trust'].config(text=f"{player_convo.trust}/1000", foreground=trust_color)
                
                # Color coding for animosity levels
                animosity_color = "red" if player_convo.animosity > 600 else "orange" if player_convo.animosity > 300 else "green"
                widgets['animosity'].config(text=f"{player_convo.animosity}/1000", foreground=animosity_color)
            else:
                widgets['trust'].config(text="500/1000", foreground="black")
                widgets['animosity'].config(text="500/1000", foreground="black")
            
            # Color coding for NPC anger
            anger_color = "red" if person.anger > 600 else "orange" if person.anger > 300 else "green"
            widgets['anger'].config(text=f"{person.anger}/1000", foreground=anger_color)
    
    def simulation_tick(self):
        """Execute one simulation tick"""
        self.log_output(f"\n🎯 TICK {self.tick_count + 1}")
        self.log_output("-" * 30)
        
        # Store previous state for comparison
        prev_conversations = set()
        for conv in self.sim.conversations.values():
            conv_key = tuple(sorted(p.name for p in conv.participants))
            prev_conversations.add(conv_key)
        
        prev_anger = {p.name: p.anger for p in self.sim.people.values()}
        
        # Execute tick
        self.sim.tick()
        self.tick_count += 1
        
        # Check for changes and log them
        self.log_changes(prev_conversations, prev_anger)
        
        # Update display
        self.update_display()
        
    def log_changes(self, prev_conversations, prev_anger):
        """Log changes that occurred during the tick"""
        changes_logged = False
        
        # Check for new/ended conversations
        curr_conversations = set()
        for conv in self.sim.conversations.values():
            conv_key = tuple(sorted(p.name for p in conv.participants))
            curr_conversations.add(conv_key)
        
        new_convs = curr_conversations - prev_conversations
        ended_convs = prev_conversations - curr_conversations
        
        if new_convs:
            changes_logged = True
            self.log_output("🗣️ NEW CONVERSATIONS:")
            for conv_key in new_convs:
                self.log_output(f"   {' and '.join(conv_key)} started talking")
        
        if ended_convs:
            changes_logged = True
            self.log_output("🚶 ENDED CONVERSATIONS:")
            for conv_key in ended_convs:
                self.log_output(f"   {' and '.join(conv_key)} stopped talking")
        
        # Check for anger changes
        for person in self.sim.people.values():
            if abs(person.anger - prev_anger[person.name]) > 50:
                changes_logged = True
                emotion = "😡" if person.anger > prev_anger[person.name] else "😌"
                self.log_output(f"{emotion} {person.name}'s anger changed: {prev_anger[person.name]} → {person.anger}")
        
        # Check for fights
        for rel in self.sim.relationships.values():
            if self.sim.check_for_fight(rel):
                changes_logged = True
                self.log_output(f"⚔️ FIGHT: {rel.person1.name} and {rel.person2.name} are fighting!")
        
        if not changes_logged:
            self.log_output("😴 Nothing significant happened this tick")
    
    def send_message(self):
        """Send message to selected NPC"""
        message = self.message_entry.get().strip()
        npc_name = self.selected_npc.get()
        
        if not message:
            messagebox.showwarning("Empty Message", "Please enter a message to send.")
            return
        
        if not npc_name:
            messagebox.showwarning("No NPC Selected", "Please select an NPC to talk to.")
            return
        
        # Find the NPC
        npc = None
        for person in self.sim.people.values():
            if person.name == npc_name:
                npc = person
                break
        
        if not npc:
            messagebox.showerror("NPC Not Found", f"Could not find NPC named {npc_name}")
            return
        
        # Log the conversation
        self.log_output(f"\n💬 CONVERSATION WITH {npc_name.upper()}")
        self.log_output(f"You: {message}")
        
        try:
            # Use the simulation's talk functionality
            response = self.sim.talk_to_player(npc.id, message)
            print(response)
            if response:
                self.log_output(f"{npc_name}: {response}")
            else:
                self.log_output(f"{npc_name}: *looks at you confused*")
                self.log_output("(The NPC seems to have trouble understanding you)")
        
        except Exception as e:
            self.log_output(f"{npc_name}: *seems distracted*")
            self.log_output(f"(Error in conversation: {str(e)})")
        
        # Clear message entry
        self.message_entry.delete(0, tk.END)
        
        # Update display to show any changes
        self.update_display()
    
    def log_output(self, text):
        """Add text to the output area"""
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

def main():
    # Create the GUI
    root = tk.Tk()
    app = SimulationGUI(root)
    
    # Configure ttk styles for better appearance
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass  # Use default theme if clam is not available
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main() 