import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Textarea } from '@/components/ui/textarea';
import { saveJobPreferences, fetchProfile } from '@/lib/api';

interface JobPreferences {
  query: string;
  location: string;
  mode_of_job: string;
  work_experience: string;
  employment_types: string[];
  company_types: string[];
  job_requirements: string;
}

const JobPreferences = () => {
  const navigate = useNavigate();
  const [preferences, setPreferences] = React.useState<Partial<JobPreferences>>({
    employment_types: [],
    company_types: []
  });
  const [isLoading, setIsLoading] = React.useState(false);

  const employmentTypeOptions = [
    'Full-time',
    'Part-time',
    'Contract',
    'Temporary',
    'Internship',
    'Freelance'
  ];

  const companyTypeOptions = [
    'Startup',
    'Small Business',
    'Medium Enterprise',
    'Large Corporation',
    'Non-profit',
    'Government',
    'Consulting',
    'Agency'
  ];

  const workExperienceOptions = [
    'Entry Level (0-1 years)',
    'Junior (1-3 years)', 
    'Mid Level (3-5 years)',
    'Senior (5-8 years)',
    'Lead (8+ years)',
    'Executive (10+ years)'
  ];

  React.useEffect(() => {
    // Try to fetch existing profile data
    fetchProfile()
      .then((res) => {
        if (res.data) {
          setPreferences({
            query: res.data.query || '',
            location: res.data.location || '',
            mode_of_job: res.data.mode_of_job || '',
            work_experience: res.data.work_experience || '',
            employment_types: res.data.employment_types || [],
            company_types: res.data.company_types || [],
            job_requirements: res.data.job_requirements || ''
          });
        }
      })
      .catch((error) => {
        if (error.response?.status === 404) {
          console.log("No existing profile found, starting fresh");
        } else if (error.response?.status === 401) {
          console.error("Unauthorized access");
        } else {
          console.error("Failed to fetch profile:", error);
        }
      });
  }, []);

  const handleEmploymentTypeChange = (type: string, checked: boolean) => {
    setPreferences(prev => ({
      ...prev,
      employment_types: checked 
        ? [...(prev.employment_types || []), type]
        : (prev.employment_types || []).filter(t => t !== type)
    }));
  };

  const handleCompanyTypeChange = (type: string, checked: boolean) => {
    setPreferences(prev => ({
      ...prev,
      company_types: checked 
        ? [...(prev.company_types || []), type]
        : (prev.company_types || []).filter(t => t !== type)
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Validation
    if (!preferences.query || !preferences.location || !preferences.mode_of_job || !preferences.work_experience) {
      toast.error('Please fill in all required fields');
      return;
    }

    if (!preferences.employment_types || preferences.employment_types.length === 0) {
      toast.error('Please select at least one employment type');
      return;
    }

    setIsLoading(true);
    
    try {
      await saveJobPreferences(preferences);
      toast.success('Job preferences saved successfully!');
      navigate('/resume-upload');
    } catch (error) {
      console.error('Failed to save job preferences:', error);
      toast.error('Failed to save job preferences. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = () => {
    if (window.confirm('Skip job preferences setup? You can configure them later in your dashboard.')) {
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 hero-gradient flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Card className="w-full max-w-2xl p-8 space-y-6 glass-card animate-fade-in">
          <div className="text-center space-y-2">
            <h2 className="text-3xl font-bold">Job Preferences</h2>
            <p className="text-muted-foreground">
              Tell us about your ideal job to get better matches
            </p>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Job Title */}
            <div className="space-y-2">
              <Label htmlFor="query" className="text-sm font-medium">
                Job Title / Keywords <span className="text-red-500">*</span>
              </Label>
              <Input
                id="query"
                placeholder="e.g., Frontend Developer, Data Scientist, Product Manager"
                value={preferences.query || ''}
                onChange={(e) => setPreferences(prev => ({ ...prev, query: e.target.value }))}
                className="w-full"
              />
            </div>

            {/* Location */}
            <div className="space-y-2">
              <Label htmlFor="location" className="text-sm font-medium">
                Preferred Location <span className="text-red-500">*</span>
              </Label>
              <Input
                id="location"
                placeholder="e.g., New York, London, Remote"
                value={preferences.location || ''}
                onChange={(e) => setPreferences(prev => ({ ...prev, location: e.target.value }))}
                className="w-full"
              />
            </div>

            {/* Work Mode and Experience Level */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-sm font-medium">
                  Work Mode <span className="text-red-500">*</span>
                </Label>
                <Select
                  value={preferences.mode_of_job || ''}
                  onValueChange={(value) => setPreferences(prev => ({ ...prev, mode_of_job: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select work mode" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="remote">Remote</SelectItem>
                    <SelectItem value="hybrid">Hybrid</SelectItem>
                    <SelectItem value="in-place">On-site</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-sm font-medium">
                  Experience Level <span className="text-red-500">*</span>
                </Label>
                <Select
                  value={preferences.work_experience || ''}
                  onValueChange={(value) => setPreferences(prev => ({ ...prev, work_experience: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select experience level" />
                  </SelectTrigger>
                  <SelectContent>
                    {workExperienceOptions.map((option) => (
                      <SelectItem key={option} value={option}>
                        {option}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Employment Types */}
            <div className="space-y-3">
              <Label className="text-sm font-medium">
                Employment Types <span className="text-red-500">*</span>
              </Label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {employmentTypeOptions.map((type) => (
                  <div key={type} className="flex items-center space-x-2">
                    <Checkbox
                      id={`employment-${type}`}
                      checked={(preferences.employment_types || []).includes(type)}
                      onCheckedChange={(checked) => handleEmploymentTypeChange(type, checked as boolean)}
                    />
                    <Label htmlFor={`employment-${type}`} className="text-sm font-normal">
                      {type}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {/* Company Types */}
            <div className="space-y-3">
              <Label className="text-sm font-medium">Company Types (Optional)</Label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {companyTypeOptions.map((type) => (
                  <div key={type} className="flex items-center space-x-2">
                    <Checkbox
                      id={`company-${type}`}
                      checked={(preferences.company_types || []).includes(type)}
                      onCheckedChange={(checked) => handleCompanyTypeChange(type, checked as boolean)}
                    />
                    <Label htmlFor={`company-${type}`} className="text-sm font-normal">
                      {type}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {/* Additional Requirements */}
            <div className="space-y-2">
              <Label htmlFor="requirements" className="text-sm font-medium">
                Additional Job Requirements (Optional)
              </Label>
              <Textarea
                id="requirements"
                placeholder="e.g., Must have React experience, open to travel, need visa sponsorship..."
                value={preferences.job_requirements || ''}
                onChange={(e) => setPreferences(prev => ({ ...prev, job_requirements: e.target.value }))}
                rows={3}
                className="w-full"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex justify-between pt-6">
              <Button 
                type="button" 
                variant="outline" 
                onClick={handleSkip}
                disabled={isLoading}
              >
                Skip for Now
              </Button>
              <Button 
                type="submit" 
                disabled={isLoading}
                className="min-w-[120px]"
              >
                {isLoading ? 'Saving...' : 'Continue'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default JobPreferences;
