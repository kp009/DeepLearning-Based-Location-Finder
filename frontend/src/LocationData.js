import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LocationData = () => {
    const [locations, setLocations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({
        id: '',
        location: '',
        latitude: '',
        longitude: '',
        cost: ''
    });

    // Pagination state
    const [currentPage, setCurrentPage] = useState(1);
    const [locationsPerPage] = useState(5); // Set the number of locations per page

    useEffect(() => {
        fetchLocations();
    }, []);

    const fetchLocations = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/images/');
            const updatedLocations = await Promise.all(response.data.map(async (loc) => {
                const cost = await fetchCost(loc.latitude, loc.longitude);
                return { ...loc, cost };
            }));
            setLocations(updatedLocations);
        } catch (err) {
            setError("Failed to fetch location data.");
            console.error("Error fetching locations:", err);
        } finally {
            setLoading(false);
        }
    };

    const fetchCost = async (latitude, longitude) => {
        try {
            if (!latitude || !longitude) return 0;
            const response = await axios.get(`http://localhost:8000/api/distance/${latitude}/${longitude}/`);
            return response.data.cost.toFixed(2);
        } catch (err) {
            console.error("Error fetching cost:", err);
            return "Error";
        }
    };

    // Pagination logic
    const indexOfLastLocation = currentPage * locationsPerPage;
    const indexOfFirstLocation = indexOfLastLocation - locationsPerPage;
    const currentLocations = locations.slice(indexOfFirstLocation, indexOfLastLocation);

    const handleEditClick = (loc) => {
        setIsEditing(true);
        setEditData({
            id: loc.id,
            location: loc.location,
            latitude: loc.latitude,
            longitude: loc.longitude,
            cost: loc.cost
        });
    };

    const handleEditChange = async (e) => {
        const { name, value } = e.target;
        let updatedData = { ...editData, [name]: value };

        if (name === "latitude" || name === "longitude") {
            const updatedCost = await fetchCost(updatedData.latitude, updatedData.longitude);
            updatedData = { ...updatedData, cost: updatedCost };
        }

        setEditData(updatedData);
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.put(`http://localhost:8000/api/images/update/${editData.id}/`, editData);
            const updatedLocations = locations.map(loc =>
                loc.id === editData.id ? response.data : loc
            );
            setLocations(updatedLocations);
            setIsEditing(false);
        } catch (err) {
            setError("Failed to update location.");
            console.error("Error updating location:", err);
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:8000/api/images/delete/${id}/`);
            setLocations(locations.filter(loc => loc.id !== id));
        } catch (err) {
            setError("Failed to delete the location.");
            console.error("Error deleting location:", err);
        }
    };

    // Pagination controls
    const totalPages = Math.ceil(locations.length / locationsPerPage);

    const handleNextPage = () => {
        if (currentPage < totalPages) setCurrentPage(currentPage + 1);
    };

    const handlePrevPage = () => {
        if (currentPage > 1) setCurrentPage(currentPage - 1);
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            {isEditing ? (
                <div>
                    <h2>Edit Location</h2>
                    <form onSubmit={handleEditSubmit}>
                        <div>
                            <label>Location Name</label>
                            <input
                                type="text"
                                name="location"
                                value={editData.location}
                                onChange={handleEditChange}
                            />
                        </div>
                        <div>
                            <label>Latitude</label>
                            <input
                                type="number"
                                name="latitude"
                                value={editData.latitude}
                                onChange={handleEditChange}
                            />
                        </div>
                        <div>
                            <label>Longitude</label>
                            <input
                                type="number"
                                name="longitude"
                                value={editData.longitude}
                                onChange={handleEditChange}
                            />
                        </div>
                        <div>
                            <label>Cost</label>
                            <input
                                type="text"
                                name="cost"
                                value={editData.cost}
                                readOnly
                            />
                        </div>
                        <button type="submit">Save Changes</button>
                    </form>
                    <button onClick={() => setIsEditing(false)}>Cancel</button>
                </div>
            ) : (
                <div>
                    {locations.length === 0 ? (
                        <p>No locations available</p>
                    ) : (
                        <table border="1" style={{ width: '100%', marginTop: '20px', borderCollapse: 'collapse' }}>
                            <thead>
                                <tr>
                                    <th>Image</th>
                                    <th>Location</th>
                                    <th>Latitude</th>
                                    <th>Longitude</th>
                                    <th>Cost</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {currentLocations.map((loc) => (
                                    <tr key={loc.id}>
                                        <td>
                                            <img src={loc.image} alt={loc.location} style={{ width: '100px', height: 'auto' }} />
                                        </td>
                                        <td>{loc.location}</td>
                                        <td>{loc.latitude}</td>
                                        <td>{loc.longitude}</td>
                                        <td>${loc.cost}</td>
                                        <td>
                                            <button onClick={() => handleEditClick(loc)}>Edit</button>
                                            <button onClick={() => handleDelete(loc.id)}>Delete</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                    <div>
                        <button onClick={handlePrevPage} disabled={currentPage === 1}>Previous</button>
                        <span> Page {currentPage} of {totalPages} </span>
                        <button onClick={handleNextPage} disabled={currentPage === totalPages}>Next</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LocationData;
