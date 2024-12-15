import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function DemoVidCard(demoVidDetails) {

    const navigate = useNavigate()

    function getCookie(cname) {
        let name = cname + "=";
        let ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    console.log(demoVidDetails['vidnum'])

    const [formData, setFormData] = useState({
        u_ip_address: getCookie('usrip_address'),
        u_sr_lang: '',
        u_dest_lang: '',
        u_vnum: demoVidDetails['vidnum'],
        u_lip_q: 0,
        u_tr_q: 0,
        u_aud_q: 0,
        u_all_q: 0
    });

    // const handleChange = (e) => {
    //     const { name, value } = e.target;
    //     setFormData({ ...formData, [name]: value });
    // };

    const [lipSyncRating, setLipSyncRating] = useState(0);
    const [translationRating, setTranslationRating] = useState(0);
    const [audioRating, setAudioRating] = useState(0);
    const [overallRating, setOverallRating] = useState(0);

    const [hoverLipSync, setHoverLipSync] = useState(0);
    const [hoverTranslation, setHoverTranslation] = useState(0);
    const [hoverAudio, setHoverAudio] = useState(0);
    const [hoverOverall, setHoverOverall] = useState(0);

    const handleReview = async (e) => {
        e.preventDefault();
        // Updating the formData state with ratings before submission
        const updatedFormData = {
            ...formData,
            u_lip_q: lipSyncRating,
            u_tr_q: translationRating,
            u_aud_q: audioRating,
            u_all_q: overallRating
        };

        console.log('Sending data:', updatedFormData); // Log the updated form data to console

        try {
            const response = await fetch('/demouser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedFormData),
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Server response:', result);
                navigate('/demo/review');
            } else {
                console.error('Error sending data:', await response.text());
            }
        } catch (error) {
            console.error('Error:', error);
        }
        // navigate('/user');
    };

    const renderStars = (rating, setRating, hover, setHover) => {
        return (
            <div className="star-rating">
                {[1, 2, 3, 4, 5].map((value) => (
                    <span
                        key={value}
                        className={`star ${value <= (hover || rating) ? 'selected' : ''}`}
                        onClick={() => setRating(value)}
                        onMouseEnter={() => setHover(value)}
                        onMouseLeave={() => setHover(0)}
                    >
                        &#9733;
                    </span>
                ))}
            </div>
        );
    };

    return (
        <>
            <div id="vid-card-review">
                <div id="src-vid">
                    <video id="srcvid" src="./engvid (1).mp4" controls></video>
                </div>
                <div id="tr-vid">
                    <video id="srcvid" src="./deepgram_final.mp4" controls></video>
                </div>
                <form onSubmit={handleReview}>
                    <div id="review-vid">
                        <div id="lip-star1">
                            <div id="lip-label">Lip Sync Quality</div>
                            {renderStars(lipSyncRating, setLipSyncRating, hoverLipSync, setHoverLipSync)}
                        </div>
                        <div id="tr-star2">
                            <div id="tr-label">Translation Quality</div>
                            {renderStars(translationRating, setTranslationRating, hoverTranslation, setHoverTranslation)}
                        </div>
                        <div id="aud-star3">
                            <div id="aud-label">Audio Quality</div>
                            {renderStars(audioRating, setAudioRating, hoverAudio, setHoverAudio)}
                        </div>
                        <div id="all-star4">
                            <div id="all-label">Overall Quality</div>
                            {renderStars(overallRating, setOverallRating, hoverOverall, setHoverOverall)}
                        </div>
                    </div>
                    <button type="submit">Submit Review</button>
                </form>
            </div>
        </>
    )
}

export default DemoVidCard