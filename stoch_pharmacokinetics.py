import numpy as np 
import matplotlib.pyplot as plt

def simulate_drug_concentration(n_hours, dose_mg, absorption_rate, elimination_rate):
    """
    Simulates drug concentration in the bloodstream using a One-Compartment PK Model.
    
    Parameters:
    - n_hours: Duration of simulation
    - dose_mg: Initial dosage
    - absorption_rate (ka): Rate at which drug enters the blood
    - elimination_rate (ke): Rate at which the body clears the drug
    """
    dt = 0.1  # 6-minute increments
    steps = int(n_hours / dt)
    time_axis = np.linspace(0, n_hours, steps)
    concentration = np.zeros(steps)
    
    # Stochastic 'Metabolic Noise' (Brownian Motion component)
    noise_scale = 0.05
    
    for t in range(1, steps):
        # The PK Differential Equation: 
        # dC = [ka * Dose * e^(-ka*t) - ke * C] * dt + Noise
        
        # 1. Input Signal: Exponential absorption from the gut
        input_signal = absorption_rate * dose_mg * np.exp(-absorption_rate * (t * dt))
        
        # 2. Elimination: First-order decay
        decay = elimination_rate * concentration[t-1]
        
        # 3. Numerical Integration (Euler Method)
        change = (input_signal - decay) * dt
        noise = np.random.normal(0, noise_scale)
        
        # Update state, ensuring concentration cannot be negative
        concentration[t] = max(0, concentration[t-1] + change + noise)
        
    return time_axis, concentration

# --- EXECUTION & SIMULATION ---
N_HOURS = 24
DOSE = 100
KA = 1.2    # Absorption
KE = 0.15   # Elimination

time, path = simulate_drug_concentration(N_HOURS, DOSE, KA, KE)

# --- ANALYTICS ---
c_max = np.max(path)
t_max = np.argmax(path) * 0.1
final_level = path[-1]

print(f"--- 🧪 QUANTITATIVE MEDICINE: PK MODEL ---")
print(f"Peak Concentration (Cmax): {c_max:.2f} mg/L")
print(f"Time to Peak (Tmax): {t_max:.1f} hours")
print(f"Final Residual Level: {final_level:.2f} mg/L")
print("-" * 45)
print("Isomorphism Note: This decay curve models both biological")
print("metabolism and the 'Market Impact' of a trade block.")

# --- VISUALIZATION ---
plt.figure(figsize=(10, 5))
plt.plot(time, path, color='#008080', linewidth=2, label='Drug Concentration')

# Style adjustments for a professional "Quant" look
plt.fill_between(time, path, color='#008080', alpha=0.1)
plt.axvline(x=t_max, color='red', linestyle='--', alpha=0.5, label=f'Peak at {t_max}h')
plt.title('Pharmacokinetic Stochastic Simulation (SDE)', fontsize=14)
plt.xlabel('Time (Hours)', fontsize=12)
plt.ylabel('Concentration (mg/L)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

# Save the plot for GitHub
# plt.savefig('pk_simulation_results.png') 
plt.show()
