
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Save, X } from "lucide-react";
import ViewPreferencesContent from './ViewPreferencesContent';
import EditPreferencesForm from './EditPreferencesForm';

const JobPreferences = () => {
  const [editing, setEditing] = useState(false);
  const [preferences, setPreferences] = useState({
    roles: ["Front-End Developer", "React Developer", "UI Engineer"],
    locations: ["San Francisco, CA", "Remote"],
    workMode: "Hybrid",
    skills: ["React", "TypeScript", "Tailwind CSS", "Node.js"],
    experienceLevel: "Mid-Level",
    salaryExpectation: "$90,000 - $120,000"
  });

  const [newPreferences, setNewPreferences] = useState({...preferences});
  const [newSkill, setNewSkill] = useState("");
  const [newLocation, setNewLocation] = useState("");
  const [newRole, setNewRole] = useState("");

  const handleSave = () => {
    setPreferences(newPreferences);
    setEditing(false);
  };

  const handleCancel = () => {
    setNewPreferences({...preferences});
    setEditing(false);
  };

  const addSkill = () => {
    if (newSkill && !newPreferences.skills.includes(newSkill)) {
      setNewPreferences({
        ...newPreferences,
        skills: [...newPreferences.skills, newSkill]
      });
      setNewSkill("");
    }
  };

  const removeSkill = (skill: string) => {
    setNewPreferences({
      ...newPreferences,
      skills: newPreferences.skills.filter(s => s !== skill)
    });
  };

  const addLocation = () => {
    if (newLocation && !newPreferences.locations.includes(newLocation)) {
      setNewPreferences({
        ...newPreferences,
        locations: [...newPreferences.locations, newLocation]
      });
      setNewLocation("");
    }
  };

  const removeLocation = (location: string) => {
    setNewPreferences({
      ...newPreferences,
      locations: newPreferences.locations.filter(l => l !== location)
    });
  };

  const addRole = () => {
    if (newRole && !newPreferences.roles.includes(newRole)) {
      setNewPreferences({
        ...newPreferences,
        roles: [...newPreferences.roles, newRole]
      });
      setNewRole("");
    }
  };

  const removeRole = (role: string) => {
    setNewPreferences({
      ...newPreferences,
      roles: newPreferences.roles.filter(r => r !== role)
    });
  };

  return (
    <Card className="mb-6">
      <CardHeader className="pb-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-xl font-semibold">Job Preferences</CardTitle>
          <CardDescription>Settings for your job search</CardDescription>
        </div>
        {!editing ? (
          <Button 
            onClick={() => setEditing(true)} 
            variant="outline" 
            size="sm"
          >
            Edit Preferences
          </Button>
        ) : (
          <div className="flex gap-2">
            <Button 
              onClick={handleSave} 
              size="sm"
              className="flex items-center gap-1"
            >
              <Save className="h-4 w-4" />
              Save
            </Button>
            <Button 
              onClick={handleCancel} 
              variant="outline" 
              size="sm"
              className="flex items-center gap-1"
            >
              <X className="h-4 w-4" />
              Cancel
            </Button>
          </div>
        )}
      </CardHeader>
      
      <CardContent>
        {!editing ? (
          <ViewPreferencesContent preferences={preferences} />
        ) : (
          <EditPreferencesForm 
            preferences={newPreferences}
            onPreferencesChange={setNewPreferences}
            newRole={newRole}
            setNewRole={setNewRole}
            newLocation={newLocation}
            setNewLocation={setNewLocation}
            newSkill={newSkill}
            setNewSkill={setNewSkill}
            addRole={addRole}
            removeRole={removeRole}
            addLocation={addLocation}
            removeLocation={removeLocation}
            addSkill={addSkill}
            removeSkill={removeSkill}
          />
        )}
      </CardContent>
    </Card>
  );
};

export default JobPreferences;
