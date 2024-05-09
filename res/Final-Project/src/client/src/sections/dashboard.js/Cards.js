import React from 'react';
import PropTypes from 'prop-types';
import { Grid } from '@mui/material';
import CardStructure from './CardStructure';

export default function Cards(props) {
  return (
    <div>
      <Grid container spacing={3} display="flex" marginTop={-4.5}>
        <Grid item xs={12} sm={6} md={3}>
          <CardStructure title="Total budget" icon={'mdi:money'} val={'596.B'} />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <CardStructure
            title="Votes amount"
            color="info"
            icon={'game-icons:vote'}
            val={props.voters ? props.voters : '0'}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <CardStructure title="The biggest office" color="warning" icon={'ep:office-building'} val={'ש.חברתיים'} />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <CardStructure title="Number of Projects" color="error" icon={'file-icons:microsoft-project'} val={'4867'} />
        </Grid>
      </Grid>
    </div>
  );
}

Cards.propTypes = { voters: PropTypes.string };
