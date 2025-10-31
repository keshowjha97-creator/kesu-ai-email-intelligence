'use client';

import { useEffect, useState } from 'react';
import { Mail, TrendingUp, Clock, Calendar, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalEmails: 0,
    priorityEmails: 0,
    actionRequired: 0,
    meetings: 0,
    timeSaved: 0
  });

  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch from API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/analysis/dashboard`);
      const data = await response.json();
      
      setStats(data.stats);
      setEmails(data.emails);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your email intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Email Intelligence Dashboard</h1>
          <p className="text-gray-600 mt-2">Your AI-powered email insights</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <StatCard
            icon={<Mail className="w-6 h-6" />}
            title="Total Emails"
            value={stats.totalEmails}
            color="blue"
          />
          <StatCard
            icon={<AlertCircle className="w-6 h-6" />}
            title="Priority"
            value={stats.priorityEmails}
            color="red"
          />
          <StatCard
            icon={<TrendingUp className="w-6 h-6" />}
            title="Action Required"
            value={stats.actionRequired}
            color="orange"
          />
          <StatCard
            icon={<Calendar className="w-6 h-6" />}
            title="Meetings"
            value={stats.meetings}
            color="green"
          />
          <StatCard
            icon={<Clock className="w-6 h-6" />}
            title="Time Saved"
            value={`${stats.timeSaved}h`}
            color="purple"
          />
        </div>

        {/* Email List */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Priority Emails</h2>
          <div className="space-y-4">
            {emails.slice(0, 10).map((email, index) => (
              <EmailCard key={index} email={email} />
            ))}
          </div>
        </div>

        {/* Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Email Activity</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[
              { name: 'Mon', emails: 45 },
              { name: 'Tue', emails: 52 },
              { name: 'Wed', emails: 38 },
              { name: 'Thu', emails: 61 },
              { name: 'Fri', emails: 48 },
              { name: 'Sat', emails: 12 },
              { name: 'Sun', emails: 8 }
            ]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="emails" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value, color }) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    red: 'bg-red-100 text-red-600',
    orange: 'bg-orange-100 text-orange-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600'
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className={`inline-flex p-3 rounded-lg ${colorClasses[color]} mb-4`}>
        {icon}
      </div>
      <p className="text-gray-600 text-sm">{title}</p>
      <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
    </div>
  );
}

function EmailCard({ email }) {
  const priorityColors = {
    High: 'bg-red-100 text-red-800',
    Medium: 'bg-yellow-100 text-yellow-800',
    Low: 'bg-green-100 text-green-800'
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className={`px-2 py-1 rounded text-xs font-medium ${priorityColors[email.priority]}`}>
              {email.priority}
            </span>
            <span className="text-xs text-gray-500">{email.category}</span>
          </div>
          <h3 className="font-semibold text-gray-900 mb-1">{email.subject}</h3>
          <p className="text-sm text-gray-600 mb-2">{email.from}</p>
          <p className="text-sm text-gray-500">{email.summary}</p>
        </div>
        <div className="text-xs text-gray-400">{email.date}</div>
      </div>
    </div>
  );
}
