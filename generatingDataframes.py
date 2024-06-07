import pandas as pd
import os

# Path to the folders
recorded_path = 'C:/Path/to/recorded/data'
supposed_path = 'C:/Path/to/annotated/data'
save_path = 'C:/Path/to/save/pickles'


# Initialize an empty DataFrame to collect the data
data = []

# Iterate through each file in the folder
for filename in os.listdir(recorded_path):
    if filename.endswith(".txt"):
        
        # Extract frame number from the filename
        frame_number = int(filename.split('_')[-1].split('.')[0])
        
        # Read the content of the file
        with open(os.path.join(recorded_path, filename), 'r') as file:
            for line in file:
                
                components = line.split()
                class_id = int(components[0])
                x_center = float(components[1])
                y_center = float(components[2])
                width = float(components[3])
                height = float(components[4])
                confidence = float(components[5])
                    
                # Append data to the list
                data.append({
                    'frame_number': frame_number,
                    'tip_detected': 1,
                    'x_coordinate': x_center,
                    'y_coordinate': y_center,
                    'width': width,
                    'height': height,
                    'confidence': confidence
                })
                
                
                

# Create a DataFrame from the recorded data
df_recorded = pd.DataFrame(data)
print(df_recorded.head())
df_recorded = df_recorded.sort_values(by='frame_number')
for i in (1,df_recorded['frame_number'].values[-1]):
    if i not in df_recorded['frame_number'].values:
        print(i)
        df_recorded.loc[len(df_recorded), df_recorded.columns] = i,0,0,0,0,0,0
        
# Empty data
data = []

# Iterate through each file in the folder
for filename in os.listdir(supposed_path):
    if filename.endswith(".txt"):
        # Extract frame number from the filename
        frame_number = int(filename.split('_')[-1].split('.')[0])
        
        # Read the content of the file
        with open(os.path.join(supposed_path, filename), 'r') as file:
            for line in file:
                
                components = line.split()
                class_id = int(components[0])
                x_center = float(components[1])
                y_center = float(components[2])
                width = float(components[3])
                height = float(components[4])
                    
                # Append data to the list
                data.append({
                    'frame_number': frame_number,
                    'tip_detected': 1,
                    'x_coordinate': x_center,
                    'y_coordinate': y_center,
                    'width': width,
                    'height': height, 
                })

# Create a DataFrame from the annotated data
df_supposed = pd.DataFrame(data)
df_supposed = df_supposed.sort_values(by='frame_number')
for i in (1,df_supposed['frame_number'].values[-1]):
    if i not in df_supposed['frame_number'].values:
        print(i)
        df_supposed.loc[len(df_supposed), df_supposed.columns] = i,0,0,0,0,0








def is_center_inside_box(x_center, y_center, box_x, box_y, box_width, box_height):
    return (x_center >= box_x - box_width / 2) and \
           (x_center <= box_x + box_width / 2) and \
           (y_center >= box_y - box_height / 2) and \
           (y_center <= box_y + box_height / 2)

# Group by frame_number
grouped_recorded = df_recorded.groupby('frame_number')
grouped_supposed = df_supposed.groupby('frame_number')

# List to store results
results = []

# Iterate over each group
for frame_number, recorded_group in grouped_recorded:
    supposed_group = grouped_supposed.get_group(frame_number)
    
    # Cartesian product to compare every combination of recorded and supposed entries for this frame_number
    for _, recorded_row in recorded_group.iterrows():
        for _, supposed_row in supposed_group.iterrows():
            center_inside_box = is_center_inside_box(recorded_row['x_coordinate'], recorded_row['y_coordinate'],
                                                     supposed_row['x_coordinate'], supposed_row['y_coordinate'],
                                                     supposed_row['width'], supposed_row['height'])
            results.append({'frame_number': frame_number,
                            'tip_detected_recorded': recorded_row['tip_detected'],
                            'tip_detected_supposed': supposed_row['tip_detected'],
                            'center_inside_box': center_inside_box})

# Convert results to DataFrame
results_df = pd.DataFrame(results)
results_df['center_inside_box'] = results_df['center_inside_box'].astype(int)

# Now results_df will contain a row for each comparison with a column indicating if the center is inside the supposed box
print(results_df.head())

# Export to .pkl files
df_supposed.to_pickle(save_path+'df_supposed.pkl')
df_recorded.to_pickle(save_path+'df_recorded.pkl')
results_df.to_pickle(save_path+'results_df.pkl')
