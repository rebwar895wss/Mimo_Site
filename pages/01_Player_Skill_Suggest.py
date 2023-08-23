
import pandas as pd
import numpy as np
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

sset = ['Acrobatic Clear',
 'Acrobatic Finishing',
 'Aerial Superiority',
 'Blocker',
 'Captaincy',
 'Chip Shot Control',
 'Chop Turn',
 'Cut Behind &; Turn',
 'Dipping Shot',
 'Double Touch',
 'Fighting Spirit',
 'First-time Shot',
 'Flip Flap',
 'GK High Punt',
 'GK Long Throw',
 'GK Low Punt',
 'GK Penalty Saver',
 'Gamesmanship',
 'Heading',
 'Heel Trick',
 'Interception',
 'Knuckle Shot',
 'Long-Range Shooting',
 'Long-Range Curler',
 'Low Lofted Pass',
 'Man Marking',
 'Marseille Turn',
 'No Look Pass',
 'One-touch Pass',
 'Outside Curler',
 'Penalty Specialist',
 'Pinpoint Crossing',
 'Rabona',
 'Rising Shot',
 'Scissors Feint',
 'Scotch Move',
 'Sliding Tackle',
 'Sole Control',
 'Sombrero',
 'Super-sub',
 'Through Passing',
 'Track Back',
 'Weighted Pass']

def find_top_skills(pdf):
    for skill in sset:
        pdf['pred_'+skill] *= (pdf['s_'+skill]==0)
    pred_cols = [i for i in pdf.columns if 'pred_' in i]
    top_n = np.argsort(pdf[pred_cols])[0][::-1]
    top_score = np.sort(pdf[pred_cols])[0][::-1]

    sdf = pd.DataFrame(list(zip([i.lstrip('pred_') for i in np.array(pred_cols)[top_n]],top_score)), \
    columns = ['Suggested Skill','Mimo Skill Score'])
    return sdf[sdf['Mimo Skill Score']>=10]

common_picks = [89074400628164, 87964419886766, 87964420017613, 105592039524159, 105592039515849, 105592039537935]

def main():
    st.set_page_config(layout="centered")
    st.title("Mimo Skill Suggest")
    st.write('Powered by :orange[Mimo Skill Fit Score]')
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/mimo_dataset.csv')
    adf = st.session_state['df']
    adf['Player ID'] = adf['Player ID'].astype(str)

    st.write('Player ID is a number unique to each player in the game. You can obtain the player ID of each card from the URL of any Database website such as \
    [PESDB](https://pesdb.net/pes2022/) or [EFHub](https://efootballhub.net/efootball23).')
    pid = st.text_input("Enter Player ID:")
    if pid:
        pdf = adf[adf['Player ID']==pid]
        if(pdf.shape[0]>0):
            st.subheader("{} - {} {}".format(pdf['Player Name'].values[0],\
            pdf['Overall Rating'].values[0],\
            pdf['Position'].values[0]))
            st.write("Pack: {}".format(pdf['pack'].values[0].lstrip(' ')))
            st.write("Playstyle: {}".format(pdf['Playstyle'].values[0]))
            if('POTW' in pdf['pack'].values[0][1:]):
                st.write('POTW player cannot have skill added.')


            st.dataframe(find_top_skills(pdf), hide_index  = False)
            
        else:
            st.write('Player {} not found.'.format(pid))

    st.write('Example Player ID:')
    st.write(adf[adf['Player ID'].isin([str(i) for i in common_picks])][['Player ID', 'Overall Rating','Player Name','pack']].reset_index(drop = True))

            
    

if __name__ == "__main__":
    main()