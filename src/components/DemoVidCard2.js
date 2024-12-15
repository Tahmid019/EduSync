import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import sven1 from "./videos/sven1.mp4";
import sven2 from "./videos/sven2.mp4";
import svte1 from "./videos/svte1.mp4";
import svbn1 from "./videos/svbn1.mp4";
import svhi1 from "./videos/svhi1.mp4";
import dvenhi1 from "./videos/dvenhi1.mp4"
import dvenbn1 from "./videos/dvenbn1.mp4"
import dvente1 from "./videos/dvente1.mp4"
import dvenne1 from "./videos/dvenne1.mp4"
import dvenhi2 from "./videos/dvenhi2.mp4"
import dvenbn2 from "./videos/dvenbn2.mp4"
import dvente2 from "./videos/dvente2.mp4"
import dvenne2 from "./videos/dvenne2.mp4"
import dvhien1 from "./videos/dvhien1.mp4"
import dvhibn1 from "./videos/dvhibn1.mp4"
import dvhite1 from "./videos/dvhite1.mp4"
import dvbnen1 from "./videos/dvbnen1.mp4"
import dvbnhi1 from "./videos/dvbnhi1.mp4"
import dvbnte1 from "./videos/dvbnte1.mp4"
import dvteen1 from "./videos/dvteen1.mp4"
import dvtehi1 from "./videos/dvtehi1.mp4"
import dvtebn1 from "./videos/dvtebn1.mp4"

function DemoVidCard(demoVidDetails) {
    const navigate = useNavigate();

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

    const [formData, setFormData] = useState({
        u_ip_address: getCookie('usrip_address'),
        u_sr_lang: demoVidDetails.vsrlang,
        u_dest_lang: demoVidDetails.vdestlang,
        u_lip_q: demoVidDetails.u_lip_q,
        u_tr_q: demoVidDetails.u_tr_q,
        u_aud_q: demoVidDetails.u_aud_q,
        u_all_q: demoVidDetails.u_all_q
    });

    const [lipSyncRating, setLipSyncRating] = useState(demoVidDetails.u_lip_q);
    const [translationRating, setTranslationRating] = useState(demoVidDetails.u_tr_q);
    const [audioRating, setAudioRating] = useState(demoVidDetails.u_aud_q);
    const [overallRating, setOverallRating] = useState(demoVidDetails.u_all_q);

    const [hoverLipSync, setHoverLipSync] = useState(0);
    const [hoverTranslation, setHoverTranslation] = useState(0);
    const [hoverAudio, setHoverAudio] = useState(0);
    const [hoverOverall, setHoverOverall] = useState(0);

    const [srvid, setsrvid] = useState(sven1);
    const [destvid, setdestvid] = useState(dvenhi1);

    const handleReview = async (e) => {
        e.preventDefault();
        const updatedFormData = {
            ...formData,
            u_lip_q: lipSyncRating,
            u_tr_q: translationRating,
            u_aud_q: audioRating,
            u_all_q: overallRating
        };

        console.log('Sending data:', updatedFormData);

        const reviewArray = {lip: lipSyncRating, tr: translationRating, aud: audioRating, all: overallRating};

        try {
            const docRef = await addDoc(collection(db, "reviews2"), reviewArray);
            console.log("test done...");
        } catch (error) {
            console.error('Error:', error);
        }
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
        <div id="vid-card-review">
            <div id="src-vid">
                <video id="srcvid" src={srvid} controls></video>
            </div>
            <div id="tr-vid">
                <video id="destvid" src={destvid} controls></video>
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
    );
}

export default DemoVidCard;
