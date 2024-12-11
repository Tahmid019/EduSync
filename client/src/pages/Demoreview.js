// // // import React, { useState } from 'react'
// // // import { useNavigate } from 'react-router-dom';
// // // import "../css/demoreview.css"

// // // function Demoreview() {

// // //     const navigate = useNavigate
// // //     const [formData, setFormData] = useState()

// // //     function getCookie(cname) {
// // //         let name = cname + "=";
// // //         let ca = document.cookie.split(';');
// // //         for (let i = 0; i < ca.length; i++) {
// // //             let c = ca[i];
// // //             while (c.charAt(0) == ' ') {
// // //                 c = c.substring(1);
// // //             }
// // //             if (c.indexOf(name) == 0) {
// // //                 document.getElementById("")
// // //                 return c.substring(name.length, c.length);
// // //             }
// // //         }
// // //         return "";
// // //     }

// // //     const handleChange = (e) => {
// // //         const { name, value } = e.target;
// // //         setFormData({ ...formData, [name]: value });
// // //     };



// // //     const handleReview = async (e) => {
// // //         e.preventDefault(); // Prevent the default form submission behavior
// // //         if (!formData.u_mail || !formData.u_pass) {
// // //             console.error('Email and password are required');
// // //             return;
// // //         }

// // //         console.log('Sending data:', formData); // Log the form data to console

// // //         try {
// // //             const response = await fetch('/demouser', {
// // //                 method: 'POST',
// // //                 headers: {
// // //                     'Content-Type': 'application/json',
// // //                 },
// // //                 body: JSON.stringify(formData),
// // //             });

// // //             if (response.ok) {
// // //                 const result = await response.json();
// // //                 console.log('Server response:', result); // Log the server response to console
// // //                 navigate('/demo/review');
// // //             } else {
// // //                 console.error('Error sending data:', await response.text());
// // //             }
// // //         } catch (error) {
// // //             console.error('Error:', error);
// // //         }
// // //         navigate('/user')
// // //     };
// // //     var usrip = getCookie('usrip_address')
// // //     console.log("ip:")
// // //     console.log(usrip)


// // //     // const response = await axios.get('https://api.ipify.org?format=json');
// // //     // const userIp = response.data.ip;

// // //     // const postData = {
// // //     //     video: video,
// // //     //     rating: rating,
// // //     //     ip: userIp
// // //     // };

// // //     // // Send data to the backend
// // //     // await axios.post('/submit-rating', postData);


// // //     return (
// // //         <div id="rating-container">
// // //             <div id="demo-filters-section">
// // //                 <div id="f-sr-lang">
// // //                     <span>Source Language : </span><br />
// // //                     <select name="srlang" id="sr-vid-lang">
// // //                         <option value="">--Choose--</option>
// // //                         <option value="en">English</option>
// // //                         <option value="bn">Bengali</option>
// // //                         <option value="hi">Hindi</option>
// // //                         <option value="te">Telegu</option>
// // //                         <option value="ne">Nepali</option>
// // //                     </select>
// // //                 </div>
// // //                 <div id="f-dest-lang">
// // //                     <span>Translation Language : </span><br />
// // //                     <select name="destlang" id="dest-vid-lang">
// // //                         <option value="">--Choose--</option>
// // //                         <option value="en">English</option>
// // //                         <option value="bn">Bengali</option>
// // //                         <option value="hi">Hindi</option>
// // //                         <option value="te">Telegu</option>
// // //                         <option value="ne">Nepali</option>
// // //                     </select>
// // //                 </div>
// // //                 <button id="btn-submit">Apply filters</button>
// // //             </div>
// // //             <div id="vid-display">
// // //                 <div id="vid-card-review">
// // //                     <div id="src-vid">
// // //                         <video id="srcvid" src="./engvid (1).mp4" controls></video>
// // //                     </div>
// // //                     <div id="tr-vid">
// // //                         <video id="srcvid" src="./deepgram_final.mp4" controls></video>
// // //                     </div>
// // //                     <form onSubmit={handleReview}>
// // //                         <div id="review-vid">
// // //                             <div id="lip-star1">
// // //                                 <div id="lip-label">Lip Sync Qulity</div>
// // //                                 <div id="star-cnt">
// // //                                     <span id="star1">&#9733;</span>
// // //                                     <span id="star2">&#9733;</span>
// // //                                     <span id="star3">&#9733;</span>
// // //                                     <span id="star4">&#9733;</span>
// // //                                     <span id="star5">&#9733;</span>
// // //                                 </div>
// // //                             </div>
// // //                             <div id="tr-star2">
// // //                                 <div id="tr-label">Translation Qulity</div>
// // //                                 <div id="star-cnt">
// // //                                     <span id="star1">&#9733;</span>
// // //                                     <span id="star2">&#9733;</span>
// // //                                     <span id="star3">&#9733;</span>
// // //                                     <span id="star4">&#9733;</span>
// // //                                     <span id="star5">&#9733;</span>
// // //                                 </div>
// // //                             </div>
// // //                             <div id="aud-star3">
// // //                                 <div id="aud-label">Audio Qulity</div>
// // //                                 <div id="star-cnt">
// // //                                     <span id="star1">&#9733;</span>
// // //                                     <span id="star2">&#9733;</span>
// // //                                     <span id="star3">&#9733;</span>
// // //                                     <span id="star4">&#9733;</span>
// // //                                     <span id="star5">&#9733;</span>
// // //                                 </div>
// // //                             </div>
// // //                             <div id="all-star4">
// // //                                 <div id="all-label">Overall Qulity</div>
// // //                                 <div id="star-cnt">
// // //                                     <span id="star 1">&#9733;</span>
// // //                                     <span id="star 2">&#9733;</span>
// // //                                     <span id="star 3">&#9733;</span>
// // //                                     <span id="star 4">&#9733;</span>
// // //                                     <span id="star 5">&#9733;</span>
// // //                                 </div>
// // //                             </div>
// // //                         </div>
// // //                     </form>
// // //                 </div>
// // //             </div>
// // //         </div>
// // //     )
// // // }

// // // export default Demoreview

// // //==================================================================



// // import React, { useState } from 'react';
// // import { useNavigate } from 'react-router-dom';
// // import "../css/demoreview.css"

// // function Demoreview() {
// //     const navigate = useNavigate();
// //     const [formData, setFormData] = useState({});

// //     const [lipSyncRating, setLipSyncRating] = useState(0);
// //     const [translationRating, setTranslationRating] = useState(0);
// //     const [audioRating, setAudioRating] = useState(0);
// //     const [overallRating, setOverallRating] = useState(0);

// //     const [hoverLipSync, setHoverLipSync] = useState(0);
// //     const [hoverTranslation, setHoverTranslation] = useState(0);
// //     const [hoverAudio, setHoverAudio] = useState(0);
// //     const [hoverOverall, setHoverOverall] = useState(0);

// //     function getCookie(cname) {
// //         let name = cname + "=";
// //         let ca = document.cookie.split(';');
// //         for (let i = 0; i < ca.length; i++) {
// //             let c = ca[i];
// //             while (c.charAt(0) === ' ') {
// //                 c = c.substring(1);
// //             }
// //             if (c.indexOf(name) === 0) {
// //                 return c.substring(name.length, c.length);
// //             }
// //         }
// //         return "";
// //     }

// //     const handleChange = (e) => {
// //         const { name, value } = e.target;
// //         setFormData({ ...formData, [name]: value });
// //     };

// //     const handleReview = async (e) => {
// //         e.preventDefault(); // Prevent the default form submission behavior
// //         if (!formData.u_mail || !formData.u_pass) {
// //             console.error('Email and password are required');
// //             return;
// //         }

// //         console.log('Sending data:', formData); // Log the form data to console

// //         try {
// //             const response = await fetch('/demouser', {
// //                 method: 'POST',
// //                 headers: {
// //                     'Content-Type': 'application/json',
// //                 },
// //                 body: JSON.stringify(formData),
// //             });

// //             if (response.ok) {
// //                 const result = await response.json();
// //                 console.log('Server response:', result); // Log the server response to console
// //                 navigate('/demo/review');
// //             } else {
// //                 console.error('Error sending data:', await response.text());
// //             }
// //         } catch (error) {
// //             console.error('Error:', error);
// //         }
// //         navigate('/user');
// //     };

// //     const usrip = getCookie('usrip_address');
// //     console.log("ip:");
// //     console.log(usrip);

// //     const renderStars = (rating, setRating, hover, setHover) => {
// //         return (
// //             <div className="star-rating">
// //                 {[1, 2, 3, 4, 5].map((value) => (
// //                     <span
// //                         key={value}
// //                         className={`star ${value <= (hover || rating) ? 'selected' : ''}`}
// //                         onClick={() => setRating(value)}
// //                         onMouseEnter={() => setHover(value)}
// //                         onMouseLeave={() => setHover(0)}
// //                     >
// //                         &#9733;
// //                     </span>
// //                 ))}
// //             </div>
// //         );
// //     };

// //     return (
// //         <div id="rating-container">
// //             <div id="demo-filters-section">
// //                 <div id="f-sr-lang">
// //                     <span>Source Language : </span><br />
// //                     <select name="srlang" id="sr-vid-lang" onChange={handleChange}>
// //                         <option value="">--Choose--</option>
// //                         <option value="en">English</option>
// //                         <option value="bn">Bengali</option>
// //                         <option value="hi">Hindi</option>
// //                         <option value="te">Telegu</option>
// //                         <option value="ne">Nepali</option>
// //                     </select>
// //                 </div>
// //                 <div id="f-dest-lang">
// //                     <span>Translation Language : </span><br />
// //                     <select name="destlang" id="dest-vid-lang" onChange={handleChange}>
// //                         <option value="">--Choose--</option>
// //                         <option value="en">English</option>
// //                         <option value="bn">Bengali</option>
// //                         <option value="hi">Hindi</option>
// //                         <option value="te">Telegu</option>
// //                         <option value="ne">Nepali</option>
// //                     </select>
// //                 </div>
// //                 <button id="btn-submit">Apply filters</button>
// //             </div>
// //             <div id="vid-display">
// //                 <div id="vid-card-review">
// //                     <div id="src-vid">
// //                         <video id="srcvid" src="./engvid (1).mp4" controls></video>
// //                     </div>
// //                     <div id="tr-vid">
// //                         <video id="srcvid" src="./deepgram_final.mp4" controls></video>
// //                     </div>
// //                     <form onSubmit={handleReview}>
// //                         <div id="review-vid">
// //                             <div id="lip-star1">
// //                                 <div id="lip-label">Lip Sync Quality</div>
// //                                 {renderStars(lipSyncRating, setLipSyncRating, hoverLipSync, setHoverLipSync)}
// //                             </div>
// //                             <div id="tr-star2">
// //                                 <div id="tr-label">Translation Quality</div>
// //                                 {renderStars(translationRating, setTranslationRating, hoverTranslation, setHoverTranslation)}
// //                             </div>
// //                             <div id="aud-star3">
// //                                 <div id="aud-label">Audio Quality</div>
// //                                 {renderStars(audioRating, setAudioRating, hoverAudio, setHoverAudio)}
// //                             </div>
// //                             <div id="all-star4">
// //                                 <div id="all-label">Overall Quality</div>
// //                                 {renderStars(overallRating, setOverallRating, hoverOverall, setHoverOverall)}
// //                             </div>
// //                         </div>
// //                         <button type="submit">Submit Review</button>
// //                     </form>
// //                 </div>
// //             </div>
// //         </div>
// //     );
// // }

// // export default Demoreview;



// //================




// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import "../css/demoreview.css"

// function Demoreview() {
//     const navigate = useNavigate();
//     const [formData, setFormData] = useState({
//         u_ip: getCookie('usrip_address'),
//         u_sr_lang: '',
//         u_dest_lang: '',
//         u_vnum: '',
//         u_lip_q: 0,
//         u_tr_q: 0,
//         u_aud_q: 0,
//         u_all_q: 0
//     });

//     const [lipSyncRating, setLipSyncRating] = useState(0);
//     const [translationRating, setTranslationRating] = useState(0);
//     const [audioRating, setAudioRating] = useState(0);
//     const [overallRating, setOverallRating] = useState(0);

//     const [hoverLipSync, setHoverLipSync] = useState(0);
//     const [hoverTranslation, setHoverTranslation] = useState(0);
//     const [hoverAudio, setHoverAudio] = useState(0);
//     const [hoverOverall, setHoverOverall] = useState(0);

//     function getCookie(cname) {
//         let name = cname + "=";
//         let ca = document.cookie.split(';');
//         for (let i = 0; i < ca.length; i++) {
//             let c = ca[i];
//             while (c.charAt(0) === ' ') {
//                 c = c.substring(1);
//             }
//             if (c.indexOf(name) === 0) {
//                 return c.substring(name.length, c.length);
//             }
//         }
//         return "";
//     }

//     const handleChange = (e) => {
//         const { name, value } = e.target;
//         setFormData({ ...formData, [name]: value });
//     };

//     const handleReview = async (e) => {
//         e.preventDefault();
//         setFormData({ ...formData, u_lip_q: lipSyncRating, u_tr_q: translationRating, u_aud_q: audioRating, u_all_q: overallRating });

//         try {
//             const response = await fetch('/demouser', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ ...formData, u_lip_q: lipSyncRating, u_tr_q: translationRating, u_aud_q: audioRating, u_all_q: overallRating }),
//             });

//             if (response.ok) {
//                 const result = await response.json();
//                 console.log('Server response:', result);
//                 navigate('/demo/review');
//             } else {
//                 console.error('Error sending data:', await response.text());
//             }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//         // navigate('/user');
//     };

//     const renderStars = (rating, setRating, hover, setHover) => {
//         return (
//             <div className="star-rating">
//                 {[1, 2, 3, 4, 5].map((value) => (
//                     <span
//                         key={value}
//                         className={`star ${value <= (hover || rating) ? 'selected' : ''}`}
//                         onClick={() => setRating(value)}
//                         onMouseEnter={() => setHover(value)}
//                         onMouseLeave={() => setHover(0)}
//                     >
//                         &#9733;
//                     </span>
//                 ))}
//             </div>
//         );
//     };

//     return (
//         <div id="rating-container">
//             <div id="demo-filters-section">
//                 <div id="f-sr-lang">
//                     <span>Source Language : </span><br />
//                     <select name="u_sr_lang" id="sr-vid-lang" onChange={handleChange}>
//                         <option value="">--Choose--</option>
//                         <option value="en">English</option>
//                         <option value="bn">Bengali</option>
//                         <option value="hi">Hindi</option>
//                         <option value="te">Telegu</option>
//                         <option value="ne">Nepali</option>
//                     </select>
//                 </div>
//                 <div id="f-dest-lang">
//                     <span>Translation Language : </span><br />
//                     <select name="u_dest_lang" id="dest-vid-lang" onChange={handleChange}>
//                         <option value="">--Choose--</option>
//                         <option value="en">English</option>
//                         <option value="bn">Bengali</option>
//                         <option value="hi">Hindi</option>
//                         <option value="te">Telegu</option>
//                         <option value="ne">Nepali</option>
//                     </select>
//                 </div>
//                 <button id="btn-submit">Apply filters</button>
//             </div>
//             <div id="vid-display">
//                 <div id="vid-card-review">
//                     <div id="src-vid">
//                         <video id="srcvid" src="./1_en.mp4" controls></video>
//                     </div>
//                     <div id="tr-vid">
//                         <video id="srcvid" src="./1_en_final.mp4" controls></video>
//                     </div>
//                     <form onSubmit={handleReview}>
//                         <div id="review-vid">
//                             <div id="lip-star1">
//                                 <div id="lip-label">Lip Sync Quality</div>
//                                 {renderStars(lipSyncRating, setLipSyncRating, hoverLipSync, setHoverLipSync)}
//                             </div>
//                             <div id="tr-star2">
//                                 <div id="tr-label">Translation Quality</div>
//                                 {renderStars(translationRating, setTranslationRating, hoverTranslation, setHoverTranslation)}
//                             </div>
//                             <div id="aud-star3">
//                                 <div id="aud-label">Audio Quality</div>
//                                 {renderStars(audioRating, setAudioRating, hoverAudio, setHoverAudio)}
//                             </div>
//                             <div id="all-star4">
//                                 <div id="all-label">Overall Quality</div>
//                                 {renderStars(overallRating, setOverallRating, hoverOverall, setHoverOverall)}
//                             </div>
//                         </div>
//                         <button type="submit">Submit Review</button>
//                     </form>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default Demoreview;



//=================

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../css/demoreview.css"
import DemoVidCard from './DemoVidCard';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';

function Demoreview() {
    const navigate = useNavigate();
    var u_sr_lang = 'bn', u_dest_lang = 'en'
    const [formData, setFormData] = useState({
        u_sr_lang: '',
        u_dest_lang: ''
    });

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
        try {
            const response = await fetch('/demofilter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            

            if (response.ok) {
                const result = await response.json();
                console.log(result.length,'==========================')
                let newDvids = [];
                for (let i = 0; i < result.length; i++) {
                    newDvids.push(<div>
                        <DemoVidCard
                            vidnum={result[0][0]}
                            vsrlang={formData.u_sr_lang}
                            vdestlang={formData.u_dest_lang}
                            u_vnum={result[0][0]}
                            u_lip_q={0}
                            u_tr_q={0}
                            u_aud_q={0}
                            u_all_q={0}
                        /><br /></div>
                    );
                }
                setDvids(newDvids);
                console.log('Server response:', result);
            } else {
                console.error('Error sending data:', await response.text());
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // const handleReview = async (e) => {
    //     e.preventDefault();
    //     // Updating the formData state with ratings before submission
    //     const updatedFormData = {
    //         ...formData,
    //         u_lip_q: lipSyncRating,
    //         u_tr_q: translationRating,
    //         u_aud_q: audioRating,
    //         u_all_q: overallRating
    //     };

    //     console.log('Sending data:', updatedFormData); // Log the updated form data to console

    //     try {
    //         const response = await fetch('/demouser', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify(updatedFormData),
    //         });

    //         if (response.ok) {
    //             const result = await response.json();
    //             console.log('Server response:', result);
    //             navigate('/demo/review');
    //         } else {
    //             console.error('Error sending data:', await response.text());
    //         }
    //     } catch (error) {
    //         console.error('Error:', error);
    //     }
    //     // navigate('/user');
    // };

    // const renderStars = (rating, setRating, hover, setHover) => {
    //     return (
    //         <div className="star-rating">
    //             {[1, 2, 3, 4, 5].map((value) => (
    //                 <span
    //                     key={value}
    //                     className={`star ${value <= (hover || rating) ? 'selected' : ''}`}
    //                     onClick={() => setRating(value)}
    //                     onMouseEnter={() => setHover(value)}
    //                     onMouseLeave={() => setHover(0)}
    //                 >
    //                     &#9733;
    //                 </span>
    //             ))}
    //         </div>
    //     );
    // };

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
                    <button id="btn-submit" onClick={handleClick}>Apply filters</button>
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

