import React, { useEffect, useState } from 'react';
import { Container, Grid, Paper, Typography, CircularProgress, Box } from '@mui/material';
import { analyticsService } from '../services';
import { toast } from 'react-toastify';

const DashboardPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<any>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await analyticsService.getDashboard();
        setDashboardData(response.data);
      } catch (error: any) {
        toast.error('Failed to load dashboard');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="textSecondary">Total Forms</Typography>
            <Typography variant="h5">{dashboardData?.forms?.total_forms || 0}</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="textSecondary">Total Submissions</Typography>
            <Typography variant="h5">{dashboardData?.submissions?.total_submissions || 0}</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="textSecondary">Total Users</Typography>
            <Typography variant="h5">{dashboardData?.users?.total_users || 0}</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="textSecondary">Approval Rate</Typography>
            <Typography variant="h5">
              {dashboardData?.submissions?.approval_rate || 0}%
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Forms by Type</Typography>
            {dashboardData?.forms?.forms_by_type &&
              Object.entries(dashboardData.forms.forms_by_type).map(([type, count]) => (
                <Typography key={type} variant="body2">
                  {type}: {count as number}
                </Typography>
              ))}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Submissions by Status</Typography>
            {dashboardData?.submissions?.by_status &&
              Object.entries(dashboardData.submissions.by_status).map(([status, count]) => (
                <Typography key={status} variant="body2">
                  {status}: {count as number}
                </Typography>
              ))}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Top Forms</Typography>
            {dashboardData?.forms?.top_forms?.map((form: any) => (
              <Typography key={form.id} variant="body2">
                {form.title} - {form.submissions} submissions
              </Typography>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default DashboardPage;
