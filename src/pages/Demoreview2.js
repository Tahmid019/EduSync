//=================

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../css/demoreview.css"
import DemoVidCard from '../components/DemoVidCard2';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import { db } from './Firebase';
import { collection, getDocs, query, where, doc } from 'firebase/firestore';

function Demoreview() {
    const navigate = useNavigate();
    var u_sr_lang = 'bn', u_dest_lang = 'en'
    const [formData, setFormData] = useState({
        u_sr_lang: '',
        u_dest_lang: ''
    });

    const [allReviews, setAllReviews] = useState([])

    const fetchReviews = async () => {
        const reviewCollection = collection(db, "reviews")
        const reviewSnapshot = await getDocs(reviewCollection)
        const reviewsList = reviewSnapshot.docs.map((doc) => ({
            id: doc.id,
            ...doc.data(),
        }));
        setAllReviews(reviewsList);
        console.log("review collection success...");


        // const docRef = await addDoc(collection(db, "reviews2"), reviewArray)
        // console.log("test done...")

    }

    useEffect(()=>{
        fetchReviews()
    },[])

    console.log("====" + getCookie('usrip_address') + "==========")

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

    const [dvids, setDvids] = useState([]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleClick = async (e) => {
        e.preventDefault()

        fetchReviews()
        try {
            // const response = await fetch('/demofilter', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify(formData),
            // });



            // if (response.ok) {
            //     const result = await response.json();
                console.log( '==========================')
                setDvids('')
                let newDvids = [];
                for (let i = 0; i < 5; i++) {
                    newDvids.push(<div>
                        <DemoVidCard
                            // vidnum={1}
                            vsrlang={'en'}
                            vdestlang={'bn'}
                            // sr_vid_name={1}
                            // dest_vid_name={1}
                            u_vnum={1}
                            u_lip_q={1}
                            u_tr_q={1}
                            u_aud_q={1}
                            u_all_q={1}
                        /><br /></div>
                    );
                }
                // setDvids(newDvids);
                // console.log('Server response:', result);
            // } else {
            //     console.error('Error sending data:', await response.text());
            // }
        } catch (error) {
            console.error('Error:', error);
        }
    }


    return (
        <>
            <NavBar />
            <div id="rating-container" style={{ 'marginTop': '150px' }}>
                <div id="demo-filters-section">
                    <div id="f-sr-lang">
                        <span>Source Language : </span><br />
                        <select name="u_sr_lang" id="sr-vid-lang" onChange={handleChange}>
                            <option value="">--Choose--</option>
                            <option value="en">English</option>
                            <option value="bn">Bengali</option>
                            <option value="hi">Hindi</option>
                            <option value="te">Telegu</option>
                            <option value="ne">Nepali</option>
                        </select>
                    </div>
                    <div id="f-dest-lang">
                        <span>Translation Language : </span><br />
                        <select name="u_dest_lang" id="dest-vid-lang" onChange={handleChange}>
                            <option value="">--Choose--</option>
                            <option value="en">English</option>
                            <option value="bn">Bengali</option>
                            <option value="hi">Hindi</option>
                            <option value="te">Telegu</option>
                            <option value="ne">Nepali</option>
                        </select>
                    </div>
                    <button id="btn-submit" onClick={fetchReviews}>Apply filters</button>
                </div>
                <div id="vid-display" style={{ 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center' }}>
                    {/* <div id="vid-card-review">
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
                </div> */}
                    {dvids}
                </div>
            </div>
            <Footer />
        </>
    );
}

export default Demoreview;

